# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from iprestrict import ip_utils as ipu


class GetVersionTest(TestCase):
    def test_IPV4_if_no_colons(self):
        self.assertEqual(ipu.IPv4, ipu.get_version('192.168.1.1'))

    def test_IPV6_if_both_colons_and_dots(self):
        self.assertEqual(ipu.IPv6, ipu.get_version('::ffff:129.144.52.38'))

    def test_IPV6_if_only_colons(self):
        self.assertEqual(ipu.IPv6, ipu.get_version('::'))
        self.assertEqual(ipu.IPv6, ipu.get_version('::1'))


class IPToNumberTest(TestCase):
    def test_ip_to_number_conversions(self):
        self.assertEqual(0, ipu.to_number('0.0.0.0'))
        self.assertEqual(1, ipu.to_number('0.0.0.1'))
        self.assertEqual(256, ipu.to_number('0.0.1.0'))
        self.assertEqual(65537, ipu.to_number('0.1.0.1'))
        self.assertEqual(16842753, ipu.to_number('1.1.0.1'))

    def test_ip_to_number_conversions_ipv6(self):
        self.assertEqual(1, ipu.to_number('0:0:0:0:0:0:0:1'))
        self.assertEqual(10, ipu.to_number('0:0:0:0:0:0:0:a'))
        self.assertEqual((2 ** 16) ** 7 + 10, ipu.to_number('1:0:0:0:0:0:0:a'))

        # Zero collapse syntax
        self.assertEqual(0, ipu.to_number('::'))
        self.assertEqual(1, ipu.to_number('::1'))
        self.assertEqual((2 ** 16) ** 7 + 10, ipu.to_number('1::a'))

        # Mixed syntax
        self.assertEqual(1, ipu.to_number('::0.0.0.1'))
        self.assertEqual((2 ** 16) ** 7 + 10, ipu.to_number('1::0.0.0.10'))


class NumberToIPTest(TestCase):
    def test_number_to_ip_conversions(self):
        self.assertEqual('0.0.0.0', ipu.to_ip(0))
        self.assertEqual('0.0.0.1', ipu.to_ip(1))
        self.assertEqual('0.0.1.0', ipu.to_ip(256))
        self.assertEqual('0.1.0.1', ipu.to_ip(65537))
        self.assertEqual('1.1.0.1', ipu.to_ip(16842753))

    def test_number_to_ipv6_conversions(self):
        self.assertEqual('0:0:0:0:0:0:0:0', ipu.to_ip(0, version=ipu.IPv6))
        self.assertEqual('0:0:0:0:0:0:0:1', ipu.to_ip(1, version=ipu.IPv6))
        self.assertEqual('1:0:0:0:0:0:0:a', ipu.to_ip((2 ** 16) ** 7 + 10, version=ipu.IPv6))
