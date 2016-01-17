from django.test import TestCase
from unittest import skip
from iprestrict import ip_utils as ipu


class IPToNumberTest(TestCase):
    def test_ip_to_number_conversions(self):
        self.assertEqual(0, ipu.to_number('0.0.0.0'))
        self.assertEqual(1, ipu.to_number('0.0.0.1'))
        self.assertEqual(256, ipu.to_number('0.0.1.0'))
        self.assertEqual(65537, ipu.to_number('0.1.0.1'))
        self.assertEqual(16842753, ipu.to_number('1.1.0.1'))

    @skip('IPv6 to number conversion not ready')
    def test_ip_to_number_conversions_ipv6(self):
        self.assertEqual(0, ipu.to_number('::'))


class NumberToIPTest(TestCase):
    def test_number_to_ip_conversions(self):
        self.assertEqual('0.0.0.0', ipu.to_ip(0))
        self.assertEqual('0.0.0.1', ipu.to_ip(1))
        self.assertEqual('0.0.1.0', ipu.to_ip(256))
        self.assertEqual('0.1.0.1', ipu.to_ip(65537))
        self.assertEqual('1.1.0.1', ipu.to_ip(16842753))
