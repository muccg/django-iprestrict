from django.test import TestCase

from iprestrict import models
from iprestrict import restrictor

class MiddlewareRestrictsTest(TestCase):
    '''
    When the middleware is enabled it should restrict all IPs/URLs by default.
    '''
    def setUp(self):
        models.ReloadRulesRequest.request_reload()
        #restrictor.IPRestrictor.get_instance().reload_rules()

    def assert_url_is_restricted(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def assert_ip_is_restricted(self, ip):
        response = self.client.get('', REMOTE_ADDR = ip)
        self.assertEqual(response.status_code, 403)

    def test_middleware_restricts_every_url(self):
        self.assert_url_is_restricted('')
        self.assert_url_is_restricted('/every')
        self.assert_url_is_restricted('/url')
        self.assert_url_is_restricted('/is_restricted')
        self.assert_url_is_restricted('/every/url/is_restricted')

    def test_middleware_restricts_every_ip(self):
        self.assert_ip_is_restricted('127.0.0.1')
        self.assert_ip_is_restricted('192.168.1.1')
        self.assert_ip_is_restricted('10.10.10.1')
        self.assert_ip_is_restricted('169.254.0.1')

class MiddlewareAllowsTest(TestCase):
    def setUp(self):
        localhost = models.IPGroup.objects.create(name='localhost')
        models.IPRange.objects.create(ip_group=localhost, first_ip='127.0.0.1')
        models.Rule.objects.create(url_pattern='ALL', ip_group = localhost, action='A')

    def test_middleware_allows_localhost(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 404)

    def test_middleware_restricts_other_ip(self):
        response = self.client.get('', REMOTE_ADDR = '192.168.1.1')
        self.assertEqual(response.status_code, 403)

