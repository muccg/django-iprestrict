from django.core import exceptions
from django.conf import settings
import logging
from .models import ReloadRulesRequest
from .restrictor import IPRestrictor

logger = logging.getLogger(__name__)


class IPRestrictMiddleware(object):
    restrictor = None
    trusted_proxies = None
    allow_proxies = None
    dont_reload_rules = None

    def __init__(self):
        self.restrictor = IPRestrictor()
        self.trusted_proxies = tuple(getattr(settings, 'TRUSTED_PROXIES', []))
        self.dont_reload_rules = bool(getattr(settings, 'DONT_RELOAD_RULES', False))
        self.ignore_proxy_header = bool(getattr(settings, 'IGNORE_PROXY_HEADER', False))

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
        if not self.ignore_proxy_header:
            forwarded_for = self.get_forwarded_for(request)
            if forwarded_for:
                closest_proxy = client_ip
                client_ip = forwarded_for.pop(0)
                proxies = [closest_proxy] + forwarded_for
                for proxy in proxies:
                    if proxy not in self.trusted_proxies:
                        logger.info("Client IP %s forwarded by untrusted proxy %s" % (client_ip, proxy))
                        raise exceptions.PermissionDenied
        return client_ip

    def get_forwarded_for(self, request):
        hdr = request.META.get('HTTP_X_FORWARDED_FOR')
        if hdr is not None:
            return [ip.strip() for ip in hdr.split(',')]
        else:
            return []

    def reload_rules_if_needed(self):
        last_reload_request = ReloadRulesRequest.last_request()
        if last_reload_request is not None:
            if self.restrictor.last_reload < last_reload_request:
                self.restrictor.reload_rules()
