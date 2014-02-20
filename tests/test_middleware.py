from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django.core import exceptions

from iprestrict import models
from iprestrict import restrictor
from iprestrict.middleware import IPRestrictMiddleware

from datetime import datetime

LOCAL_IP = '192.168.1.1'
PROXY = '1.1.1.1'

class MiddlewareRestrictsTest(TestCase):
    '''
    When the middleware is enabled it should restrict all IPs(but localhost)/URLs by default.
    '''
    def setUp(self):
        models.ReloadRulesRequest.request_reload()

    def assert_url_is_restricted(self, url):
        response = self.client.get(url, REMOTE_ADDR = LOCAL_IP)
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

    def test_middleware_restricts_ips(self):
        self.assert_ip_is_restricted('192.168.1.1')
        self.assert_ip_is_restricted('10.10.10.1')
        self.assert_ip_is_restricted('169.254.0.1')

    def test_middleware_allows_localhost(self):
        response = self.client.get('/some/url', REMOTE_ADDR = '127.0.0.1')
        self.assertEqual(response.status_code, 404)


def create_ip_allow_rule(ip=LOCAL_IP):
    localip = models.IPGroup.objects.create(name='localip')
    models.IPRange.objects.create(ip_group=localip, first_ip=LOCAL_IP)
    models.Rule.objects.create(url_pattern='ALL', ip_group = localip, action='A')

class MiddlewareAllowsTest(TestCase):
    def setUp(self):
        create_ip_allow_rule()
        models.ReloadRulesRequest.request_reload()

    def test_middleware_allows_localhost(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 404)

    def test_middleware_allows_ip_just_added(self):
        response = self.client.get('', REMOTE_ADDR = LOCAL_IP)
        self.assertEqual(response.status_code, 404)

    def test_middleware_restricts_other_ip(self):
        response = self.client.get('', REMOTE_ADDR = '10.1.1.1')
        self.assertEqual(response.status_code, 403)

    @override_settings(TRUSTED_PROXIES=(PROXY,), ALLOW_PROXIES=False)
    def test_middleware_allows_if_proxy_is_trusted(self):
        response = self.client.get('', REMOTE_ADDR = PROXY, HTTP_X_FORWARDED_FOR= LOCAL_IP)
        self.assertEqual(response.status_code, 404)

    def test_middleware_restricts_if_proxy_is_not_trusted(self):
        response = self.client.get('', REMOTE_ADDR = PROXY, HTTP_X_FORWARDED_FOR = LOCAL_IP)
        self.assertEqual(response.status_code, 403)

class ReloadRulesTest(TestCase):
    def setUp(self):
        create_ip_allow_rule()

    def test_reload_with_custom_command(self):
        from django.core.management import call_command
        call_command('reloadrules', verbosity=0)

        response = self.client.get('', REMOTE_ADDR = LOCAL_IP)
        self.assertEqual(response.status_code, 404)

class MiddlewareExtractClientIpTest(TestCase):
    def setUp(self):
        self.middleware = IPRestrictMiddleware()
        self.factory = RequestFactory()
 
    def test_remote_addr_only(self):
        self.middleware = IPRestrictMiddleware()
        request = self.factory.get('', REMOTE_ADDR=LOCAL_IP)

        client_ip = self.middleware.extract_client_ip(request)
        self.assertEquals(client_ip, LOCAL_IP)

    def test_remote_addr_empty(self):
        self.middleware = IPRestrictMiddleware()
        request = self.factory.get('', REMOTE_ADDR='')

        client_ip = self.middleware.extract_client_ip(request)
        self.assertEquals(client_ip, '')

    @override_settings(TRUSTED_PROXIES=(PROXY,), ALLOW_PROXIES=False)
    def test_single_proxy(self):
        self.middleware = IPRestrictMiddleware()
        request = self.factory.get('', REMOTE_ADDR=PROXY, HTTP_X_FORWARDED_FOR = LOCAL_IP)

        client_ip = self.middleware.extract_client_ip(request)
        self.assertEquals(client_ip, LOCAL_IP)

    @override_settings(TRUSTED_PROXIES=(PROXY,'2.2.2.2','4.4.4.4'), ALLOW_PROXIES=False)
    def test_multiple_proxies_one_not_trusted(self):
        self.middleware = IPRestrictMiddleware()
        proxies = ['2.2.2.2', '3.3.3.3', '4.4.4.4']
        request = self.factory.get('', REMOTE_ADDR=PROXY, 
           HTTP_X_FORWARDED_FOR = ', '.join([LOCAL_IP] + proxies))
        
        try:
            client_ip = self.middleware.extract_client_ip(request)
        except exceptions.PermissionDenied:
            pass
        else:
            self.fail('Should raise PermissionDenied exception')

    @override_settings(TRUSTED_PROXIES=(PROXY,'2.2.2.2','3.3.3.3', '4.4.4.4'), ALLOW_PROXIES=False)
    def test_multiple_proxies_all_trusted(self):
        self.middleware = IPRestrictMiddleware()
        proxies = ['2.2.2.2', '3.3.3.3', '4.4.4.4']
        request = self.factory.get('', REMOTE_ADDR=PROXY, 
           HTTP_X_FORWARDED_FOR = ', '.join([LOCAL_IP] + proxies))
        
        client_ip = self.middleware.extract_client_ip(request)
        self.assertEquals(client_ip, LOCAL_IP)

