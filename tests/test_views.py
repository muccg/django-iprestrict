from django.test import TestCase
from django.contrib.auth.models import User

from iprestrict import models


class ReloadViewTest(TestCase):
    IP = '192.168.1.1'

    def setUp(self):
        admin = User.objects.create_user('admin', 'admin@nohost.org', 'pass')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        models.ReloadRulesRequest.request_reload()

    def add_allow_rule(self):
        localip = models.IPGroup.objects.create(name='Local IP')
        models.IPRange.objects.create(ip_group=localip, first_ip=self.IP)
        models.Rule.objects.create(url_pattern='ALL', ip_group = localip, action='A')

    def test_reload_view(self):
        # This test doesn't conform to unit test best practices.
        # Unfortunately, it does depend on order so it is in one method
        # instead of 3 methods, each asserting one thing

        # 1
        response = self.client.get('', REMOTE_ADDR = self.IP)
        self.assertEqual(response.status_code, 403, 'Should be restricted')

        # 2
        self.add_allow_rule()
        response = self.client.get('', REMOTE_ADDR = self.IP)
        self.assertEqual(response.status_code, 403, 'Should still be restricted - rules have not been reloaded')

        # 3 reload rules
        # TODO I have to log in as superuser for this to work
        self.client.login(username='admin', password='pass')
        response = self.client.get('/iprestrict/reload_rules')
        response = self.client.get('', REMOTE_ADDR = self.IP)
        self.assertEqual(response.status_code, 404, 'Should be allowed now')
