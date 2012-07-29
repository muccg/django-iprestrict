from django.core import exceptions
from django.utils import log
from iprestrict.models import ReloadRulesRequest

from iprestrict import IPRestrictor

logger = log.getLogger()

class IPRestrictMiddleware(object):

    def __init__(self):
        self.restrictor = IPRestrictor()

    def process_request(self, request):
        self.reload_rules_if_needed()

        url = request.path_info
        client_ip = request.META['REMOTE_ADDR']

        if self.restrictor.is_restricted(url, client_ip):
            logger.info("Denying access of %s to %s" % (url, client_ip))
            raise exceptions.PermissionDenied

    def reload_rules_if_needed(self):
        last_reload_request = ReloadRulesRequest.last_request()
        if last_reload_request is not None:
            if self.restrictor.last_reload < last_reload_request:
                self.restrictor.reload_rules()

