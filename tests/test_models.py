from django.test import TestCase
from django.http import HttpResponseForbidden

import iprestrict
from iprestrict import models
        
class RuleTest(TestCase):
    def test_restriction_methods_for_allow_rule(self):
        rule = models.Rule(url_pattern='', action='A')
        self.assertTrue(rule.is_allowed())
        self.assertFalse(rule.is_restricted())

    def test_restiction_methods_for_deny_rule(self):
        rule = models.Rule(url_pattern='', action='D')
        self.assertFalse(rule.is_allowed())
        self.assertTrue(rule.is_restricted())

    def test_matches_url_pattern_regex(self):
        rule = models.Rule(url_pattern='^/pre/[a-d]+[/]?$')
        self.assertTrue(rule.matches_url('/pre/a/'))
        self.assertTrue(rule.matches_url('/pre/a'))
        self.assertFalse(rule.matches_url('/pre/e/'))
        self.assertFalse(rule.matches_url('/pre/a//'))

    def test_rank_is_automatically_assigned_on_creation(self):
        rule1 = models.Rule.objects.create(url_pattern='1', action='A')
        rule2 = models.Rule.objects.create(url_pattern='2', action='A')
        rule10 = models.Rule.objects.create(url_pattern='10', action='A', rank=10)
        rule11 = models.Rule.objects.create(url_pattern='10', action='A')
        self.assertEquals(rule1.rank, 1)
        self.assertEquals(rule2.rank, 2)
        self.assertEquals(rule10.rank, 10)
        self.assertEquals(rule11.rank, 11)

    def test_rank_is_not_changed_on_update(self):
        rule1 = models.Rule.objects.create(url_pattern='1', action='A')
        rule2 = models.Rule.objects.create(url_pattern='2', action='A')
        rule1.action = 'D'
        rule1.save()
        self.assertEquals(rule1.rank, 1)

class RuleWithSampleRulesTests(TestCase):
    def setUp(self):
        self.rule1 = models.Rule.objects.create(url_pattern='1', action='A')
        self.rule2 = models.Rule.objects.create(url_pattern='2', action='A')

    def test_default_order_is_by_rank(self):
        rules = models.Rule.objects.all()
        self.assertEqual(rules[0].url_pattern, '1')
        self.assertEqual(rules[1].url_pattern, '2')

    def test_move_up(self):
        self.rule2.move_up()
        rules = models.Rule.objects.all()
        self.assertEqual(rules[0].url_pattern, '2')
        self.assertEqual(rules[1].url_pattern, '1')

    def test_move_up_first_rule_does_nothing(self):
        self.rule1.move_up()
        rules = models.Rule.objects.all()
        self.assertEqual(rules[0].url_pattern, '1')
        self.assertEqual(rules[1].url_pattern, '2')

    def test_move_down(self):
        self.rule1.move_down()
        rules = models.Rule.objects.all()
        self.assertEqual(rules[0].url_pattern, '2')
        self.assertEqual(rules[1].url_pattern, '1')

    def test_move_down_below_default_rule(self):
        self.rule1.move_down()
        self.rule1.move_down()
        rules = models.Rule.objects.all()
        self.assertEqual(rules[0].url_pattern, '2')
        self.assertEqual(rules[1].url_pattern, 'ALL')
        self.assertEqual(rules[2].url_pattern, '1')


class IPGroupTest(TestCase):
    def test_first_ip_group_is_all(self):
        '''An IP definition matching all should be inserted by default'''
        all_group = models.IPGroup.objects.get(name='ALL')
        self.assertTrue(all_group.matches('192.168.1.1'))
        self.assertTrue(all_group.matches('200.200.200.200'))
        self.assertTrue(all_group.matches('1.2.3.4'))

    def test_matches_with_ranges(self):
        ipgroup = models.IPGroup.objects.create(name='Local IPs')
        iprange = models.IPRange.objects.create(ip_group=ipgroup, first_ip='192.168.1.1', last_ip='192.168.1.10')
        iprange2 = models.IPRange.objects.create(ip_group=ipgroup, first_ip='192.168.1.100', last_ip='192.168.1.110')

        ipgroup.load_ranges()

        self.assertTrue(ipgroup.matches('192.168.1.1'))
        self.assertTrue(ipgroup.matches('192.168.1.5'))
        self.assertTrue(ipgroup.matches('192.168.1.10'))
        self.assertTrue(ipgroup.matches('192.168.1.105'))
        self.assertTrue(ipgroup.matches('192.168.1.100'))
        self.assertFalse(ipgroup.matches('192.168.1.0'))
        self.assertFalse(ipgroup.matches('192.168.1.11'))
        self.assertFalse(ipgroup.matches('192.168.1.99'))

    def test_ipv6_and_ip4_are_separated(self):
        ipgroup = models.IPGroup.objects.create(name='Local IPs')
        iprange = models.IPRange.objects.create(ip_group=ipgroup, first_ip='::1')
        iprange = models.IPRange.objects.create(ip_group=ipgroup, first_ip='0.0.0.2')
        ipgroup.load_ranges()

        self.assertFalse(ipgroup.matches('0.0.0.1'))
        self.assertTrue(ipgroup.matches('0.0.0.2'))
        # TODO enable when IPv6 conversion to number works
        #self.assertFalse(ipgroup.matches('::2'))
        #self.assertTrue(ipgroup.matches('::1'))

    def test_matches_with_subnets(self):
        ipgroup = models.IPGroup.objects.create(name='Local IPs')
        iprange = models.IPRange.objects.create(ip_group=ipgroup, first_ip='192.168.1.0', cidr_prefix_length=30)

        ipgroup.load_ranges()

        self.assertTrue(ipgroup.matches('192.168.1.0'))
        self.assertTrue(ipgroup.matches('192.168.1.1'))
        self.assertTrue(ipgroup.matches('192.168.1.2'))
        self.assertTrue(ipgroup.matches('192.168.1.3'))
        self.assertFalse(ipgroup.matches('192.168.0.255'))
        self.assertFalse(ipgroup.matches('192.168.1.4'))

    def test_matches_subnet_first_ip_not_correct(self):
        ipgroup = models.IPGroup.objects.create(name='Local IPs')
        iprange = models.IPRange.objects.create(ip_group=ipgroup, 
            first_ip='192.168.1.2', # Should be '192.168.1.1'
            cidr_prefix_length=30)

        ipgroup.load_ranges()

        self.assertTrue(ipgroup.matches('192.168.1.0'))
        self.assertTrue(ipgroup.matches('192.168.1.1'))
        self.assertTrue(ipgroup.matches('192.168.1.2'))
        self.assertTrue(ipgroup.matches('192.168.1.3'))
        self.assertFalse(ipgroup.matches('192.168.0.255'))
        self.assertFalse(ipgroup.matches('192.168.1.4'))

       

