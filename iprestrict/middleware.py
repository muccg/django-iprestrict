from django.http import HttpResponseForbidden
from django.core import exceptions
from django.utils import log
from django.db.models.signals import post_save
from django.dispatch import receiver
from iprestrict.models import ReloadRulesRequest

from iprestrict import IPRestrictor

logger = log.getLogger()

class IPRestrictMiddleware(object):

    def __init__(self):
        self.restrictor = IPRestrictor.get_instance()
        #self.restrictor = IPRestrictor()

    def process_request(self, request):
        url = request.path_info
        client_ip = request.META['REMOTE_ADDR']
        if self.restrictor.is_restricted(url, client_ip):
            logger.info("Denying access of %s to %s" % (url, client_ip))
            raise exceptions.PermissionDenied

    @receiver(post_save, sender=ReloadRulesRequest)
    def signal_test(sender, **kwargs):
        IPRestrictor.get_instance().reload_rules()
