from django.test import TestCase
from django.contrib.auth.models import User

from iprestrict import admin, models


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
