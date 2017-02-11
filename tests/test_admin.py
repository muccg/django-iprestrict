# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from iprestrict import admin, models
from iprestrict.geoip import NO_COUNTRY


class IPRangeFormTest(TestCase):
    def setUp(self):
        self.all_group = models.IPGroup.objects.get(name='ALL')

    def test_empty(self):
        form_data = {}
        form = admin.IPRangeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_basic(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "192.168.1.1",
            "last_ip": "192.168.1.10",
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cidr_prefix_length(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "192.168.1.1",
            "cidr_prefix_length": 24,
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cidr_prefix_length_and_last_ip(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "192.168.1.1",
            "cidr_prefix_length": 24,
            "last_ip": "192.168.1.10",
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("CIDR", "\n".join(form.errors["__all__"]))

    # github issue #5
    def test_cidr_prefix_length_invalid(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "192.168.1.1",
            "cidr_prefix_length": 42,
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("cidr_prefix_length", form.errors)
        self.assertIn("Must be a number between", "\n".join(form.errors["cidr_prefix_length"]))

    def test_cidr_prefix_length_for_ipv6(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "::1",
            "cidr_prefix_length": 127,
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ipv6_cidr_prefix_length_invalid(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "::1",
            "cidr_prefix_length": 130,
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("cidr_prefix_length", form.errors)
        self.assertIn("Must be a number between", "\n".join(form.errors["cidr_prefix_length"]))


    def test_ip_types(self):
        form_data = {
            "ip_group": self.all_group.pk,
            "first_ip": "192.168.1.1",
            "last_ip": "fe80::9eeb:e8ff:fe0e:8a21",
        }
        form = admin.IPRangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn("__all__", form.errors)
        self.assertIn("same type", "\n".join(form.errors["__all__"]))


class IPLocationFormTest(TestCase):
    def setUp(self):
        self.group = models.LocationBasedIPGroup.objects.create(name='Test Location Group')

    def tearDown(self):
        self.group.delete()

    def with_country_codes(self, codes):
        return {
            "ip_group": self.group.pk,
            "country_codes": codes,
        }

    def assert_form_validity(self, codes, should_be_valid=True, msg=''):
        form_data = self.with_country_codes(codes)
        form = admin.IPLocationForm(data=form_data)

        if should_be_valid:
            self.assertTrue(form.is_valid(), msg)
        else:
            self.assertFalse(form.is_valid(), msg)
        return form

    def test_empty_form_not_valid(self):
        form_data = {}
        form = admin.IPLocationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_country_codes_validation(self):
        self.assert_form_validity('', False, 'country_codes should be mandatory')

        form = self.assert_form_validity('AU', msg='AU should be a valid code')
        self.assertEquals(form.cleaned_data['country_codes'], 'AU')

        form = self.assert_form_validity('au', msg='country codes are case insensitive')
        self.assertEquals(form.cleaned_data['country_codes'], 'AU')

        form = self.assert_form_validity('$@!  au 23454', msg='invalid characters should be stripped')
        self.assertEquals(form.cleaned_data['country_codes'], 'AU')

        form = self.assert_form_validity('au, hu', msg='multiple countries should be ok')
        self.assertEquals(form.cleaned_data['country_codes'], 'AU, HU')

        form = self.assert_form_validity('au123456789- @#$% hu', msg='any separator is ok')
        self.assertEquals(form.cleaned_data['country_codes'], 'AU, HU')

        form = self.assert_form_validity('hu, au, br', msg='countries should be ordered')
        self.assertEquals(form.cleaned_data['country_codes'], 'AU, BR, HU')

        self.assert_form_validity('HU, AU, ZZ', False, msg='invalid country codes should NOT be allowed')
        self.assert_form_validity(NO_COUNTRY, msg='allow special country code for IPs wo country')
