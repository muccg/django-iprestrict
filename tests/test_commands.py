# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.management.base import CommandError
from django.core.management import call_command

from iprestrict import models
from iprestrict import ip_utils as ipu


class AddIPToIPGroupTest(TestCase):
    CMD = 'add_ip_to_group'

    def setUp(self):
        self.BLACKLIST = 'Blacklist'
        self.IP1 = '192.168.222.1'
        self.IP2 = '10.10.10.10'
        self.IPv6 = '2001:db8:85a3::8a2e:0370:7334'
        self.group = models.RangeBasedIPGroup.objects.create(name=self.BLACKLIST)
        self.group = models.LocationBasedIPGroup.objects.create(name='locations')

    def assertTooFewArguments(self, exception):
        self.assertTrue('too few arguments' in str(exception) or
                        'the following arguments are required' in str(exception))

    def test_arg_ip_group_is_required(self):
        with self.assertRaises(CommandError) as cm:
            call_command(self.CMD)
        self.assertTooFewArguments(cm.exception)

    def test_args_ip_group_and_at_least_one_ip_is_required(self):
        with self.assertRaises(CommandError) as cm:
            call_command(self.CMD, self.BLACKLIST)
        self.assertTooFewArguments(cm.exception)

    def test_arg_ip_group_has_to_exist(self):
        with self.assertRaises(CommandError) as cm:
            call_command(self.CMD, 'DOES NOT EXIST', self.IP1)
        self.assertIn("doesn't exist", str(cm.exception))

    def test_arg_ip_group_has_to_be_range_based(self):
        with self.assertRaises(CommandError) as cm:
            call_command(self.CMD, 'locations', self.IP1)
        self.assertIn('only to a Range based', str(cm.exception))

    def test_arg_ip_has_to_be_a_valid_ip_address(self):
        with self.assertRaises(CommandError) as cm:
            call_command(self.CMD, self.BLACKLIST, self.IP1.replace('222', '256'))
        self.assertIn('not a valid IPv4 or IPv6', str(cm.exception))

    def test_arg_ip_group_name_is_caseinsensitive(self):
        call_command(self.CMD, 'blacklist', self.IP1)

    def test_should_add_single_ip_to_ip_group(self):
        call_command(self.CMD, self.BLACKLIST, self.IP1)
        ip_range = models.IPRange.objects.get(ip_group__name=self.BLACKLIST, first_ip=self.IP1)
        self.assertIsNone(ip_range.cidr_prefix_length)
        self.assertIsNone(ip_range.last_ip)

    def test_should_add_multiple_ips_to_ip_group(self):
        call_command(self.CMD, self.BLACKLIST, self.IP1, self.IP2)
        added = models.IPRange.objects.filter(ip_group__name=self.BLACKLIST).count()
        self.assertEqual(added, 2)

    def test_should_add_multiple_ips_both_versions_to_ip_group(self):
        call_command(self.CMD, self.BLACKLIST, self.IP1, self.IP2, self.IPv6)
        added = models.IPRange.objects.filter(ip_group__name=self.BLACKLIST).count()
        group = models.RangeBasedIPGroup.objects.get(name=self.BLACKLIST)

        self.assertEqual(added, 3)
        self.assertEqual(len(group.ranges()), 3)
        self.assertEqual(len(group.ranges(ip_type=ipu.IPv4)), 2)
        self.assertEqual(len(group.ranges(ip_type=ipu.IPv6)), 1)

    def test_should_NOT_add_ip_if_ip_already_in_group(self):
        call_command(self.CMD, self.BLACKLIST, self.IP1)
        ip_count = models.IPRange.objects.filter(ip_group__name=self.BLACKLIST).count()
        call_command(self.CMD, self.BLACKLIST, self.IP1)
        ip_count_same = models.IPRange.objects.filter(ip_group__name=self.BLACKLIST).count()
        call_command(self.CMD, self.BLACKLIST, self.IP1, self.IP2)
        ip_count_adds_other = models.IPRange.objects.filter(ip_group__name=self.BLACKLIST).count()

        self.assertEqual(ip_count, 1)
        self.assertEqual(ip_count_same, 1, "shouldn't add the same IP again")
        self.assertEqual(ip_count_adds_other, 2, "should add the other IP but not the same IP")
