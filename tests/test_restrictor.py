# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import mock

import iprestrict
from iprestrict import models


IP = '10.1.1.1'
SOME_URL = '/some/url'


class IPRestrictorDefaultRulesTest(TestCase):

    def test_restrictor_restricts_all_by_default(self):
        restr = iprestrict.IPRestrictor()
        self.assertTrue(restr.is_restricted('', IP))
        self.assertTrue(restr.is_restricted(SOME_URL, IP))

    def test_allow_all_ips_for_one_url(self):
        models.Rule.objects.create(url_pattern=SOME_URL, action='A', rank=1)
        restr = iprestrict.IPRestrictor()
        self.assertFalse(restr.is_restricted(SOME_URL, IP))
        self.assertFalse(restr.is_restricted(SOME_URL, '192.168.1.1'))

    def test_caches_rules(self):
        restr = iprestrict.IPRestrictor()
        models.Rule.objects.create(url_pattern=SOME_URL, action='A', rank=1)
        # Restrictor shouldn't read the rules dynamically
        self.assertTrue(restr.is_restricted(SOME_URL, IP))

    def test_reload_rules(self):
        restr = iprestrict.IPRestrictor()
        models.Rule.objects.create(url_pattern=SOME_URL, action='A', rank=1)
        restr.reload_rules()
        self.assertFalse(restr.is_restricted(SOME_URL, IP))


class IPRestrictorNoRulesTest(TestCase):

    def setUp(self):
        models.Rule.objects.all().delete()
        self.restrictor = iprestrict.IPRestrictor()

    def test_restrictor_does_not_do_anything_with_empty_rules_table(self):
        self.assertFalse(self.restrictor.is_restricted('', IP))
        self.assertFalse(self.restrictor.is_restricted(SOME_URL, '192.168.1.1'))

    def test_restrictor_considers_rules_by_rank(self):
        rule = models.Rule.objects.create(url_pattern='ALL', action='A', rank=2)
        rule = models.Rule.objects.create(url_pattern='/admin[/].*',  action='D', rank=1)
        restr = iprestrict.IPRestrictor()
        self.assertFalse(restr.is_restricted('/some/url', IP))
        self.assertTrue(restr.is_restricted('/admin/', IP))
        self.assertTrue(restr.is_restricted('/admin/somepage', IP))


class IPRestrictorOneUrlAllowedFromOneIpTest(TestCase):
    def setUp(self):
        localip = models.RangeBasedIPGroup.objects.create(name='localip')
        models.IPRange.objects.create(ip_group=localip, first_ip=IP)
        models.Rule.objects.create(url_pattern=SOME_URL, ip_group=localip, action='A')
        self.restrictor = iprestrict.IPRestrictor()

    def test_ip_matches_url_does_not(self):
        self.assertTrue(self.restrictor.is_restricted('', IP))

    def test_url_matches_ip_does_not(self):
        self.assertTrue(self.restrictor.is_restricted(SOME_URL, '192.168.1.1'))

    def test_both_match(self):
        self.assertFalse(self.restrictor.is_restricted(SOME_URL, IP))

    def test_reload_if_ipgroup_changed(self):
        self.assertTrue(self.restrictor.is_restricted(SOME_URL, '10.10.10.10'))
        localhost = models.RangeBasedIPGroup.objects.get(name='localhost')
        models.IPRange.objects.create(ip_group=localhost, first_ip='10.10.10.10')

        self.assertTrue(self.restrictor.is_restricted(SOME_URL, '10.10.10.10'))
        self.restrictor.reload_rules()
        self.assertFalse(self.restrictor.is_restricted(SOME_URL, '10.10.10.10'))


class IPRestrictorOneIpAllowedIfNotFromOneCountryTest(TestCase):
    def setUp(self):
        us = models.LocationBasedIPGroup.objects.create(name='US')
        models.IPLocation.objects.create(ip_group=us, country_codes='US')
        models.Rule.objects.create(url_pattern='ALL', ip_group=us, action='D')
        self.us = us

        localip = models.RangeBasedIPGroup.objects.create(name='localip')
        models.IPRange.objects.create(ip_group=localip, first_ip=IP)
        models.Rule.objects.create(url_pattern=SOME_URL, ip_group=localip, action='A')

        self.restrictor = iprestrict.IPRestrictor()

    def test_url_and_ip_match_but_country_denied(self):
        with mock.patch('iprestrict.models.geoip') as m:
            m.country_code.return_value = 'US'
            self.assertTrue(self.restrictor.is_restricted(SOME_URL, IP))

    def test_reload_if_ipgroup_changed(self):
        with mock.patch('iprestrict.models.geoip') as m:
            m.country_code.return_value = 'US'

            self.assertTrue(self.restrictor.is_restricted(SOME_URL, IP))
            location = self.us.iplocation_set.first()
            location.country_codes = 'CU'
            location.save()

            self.assertTrue(self.restrictor.is_restricted(SOME_URL, IP))
            self.restrictor.reload_rules()
            self.assertFalse(self.restrictor.is_restricted(SOME_URL, IP))


class IPRestrictorReversedLocationBasedIPGroupTest(TestCase):
    def setUp(self):
        au = models.LocationBasedIPGroup.objects.create(name='Australian IPs')
        models.IPLocation.objects.create(ip_group=au, country_codes='AU')
        # Deny non-AU IP addresses
        models.Rule.objects.create(url_pattern='ALL', ip_group=au, reverse_ip_group=True, action='D')

        # Additionally allow just requests from localip
        localip = models.RangeBasedIPGroup.objects.create(name='localip')
        models.IPRange.objects.create(ip_group=localip, first_ip=IP)
        models.Rule.objects.create(url_pattern=SOME_URL, ip_group=localip, action='A')

        self.restrictor = iprestrict.IPRestrictor()

    def test_url_and_ip_match_country_denied_then_allowed(self):
        with mock.patch('iprestrict.models.geoip') as m:
            m.country_code.return_value = 'US'
            self.assertTrue(self.restrictor.is_restricted(SOME_URL, IP))
            m.country_code.return_value = 'AU'
            self.assertFalse(self.restrictor.is_restricted(SOME_URL, IP))
