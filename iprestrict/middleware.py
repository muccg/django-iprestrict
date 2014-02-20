from django.core import exceptions
from django.utils import log
from iprestrict.models import ReloadRulesRequest

from iprestrict import IPRestrictor

from django.conf import settings

logger = log.getLogger(__name__)

class IPRestrictMiddleware(object):

    def __init__(self):
        self.restrictor = IPRestrictor()
        self.trusted_proxies = getattr(settings, 'TRUSTED_PROXIES', tuple())
        self.dont_reload_rules = getattr(settings, 'DONT_RELOAD_RULES', False)
        self.allow_proxies = getattr(settings, 'ALLOW_PROXIES', True)

    def process_request(self, request):
        if not self.dont_reload_rules:
            self.reload_rules_if_needed()

        url = request.path_info
        client_ip = self.extract_client_ip(request)

        if self.restrictor.is_restricted(url, client_ip):
            logger.info("Denying access of %s to %s" % (url, client_ip))
            raise exceptions.PermissionDenied

    def extract_client_ip(self, request):
        client_ip = request.META['REMOTE_ADDR']
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if self.allow_proxies:
            if not client_ip.strip():
                client_ip = forwarded_for.split(',')[0].strip()
        else:
            if forwarded_for is not None:
                forwarded_for = [ip.strip() for ip in forwarded_for.split(',')]
                closest_proxy = client_ip
                client_ip = forwarded_for.pop(0)
                proxies = [closest_proxy] + forwarded_for
                for proxy in proxies:
                    if proxy not in self.trusted_proxies:
                        logger.info("Client IP %s forwarded by untrusted proxy %s"
                            % (client_ip, proxy))
                        raise exceptions.PermissionDenied 
        return client_ip

    def reload_rules_if_needed(self):
        last_reload_request = ReloadRulesRequest.last_request()
        if last_reload_request is not None:
            if self.restrictor.last_reload < last_reload_request:
                self.restrictor.reload_rules()

