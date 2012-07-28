from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from iprestrict import models
from iprestrict.restrictor import IPRestrictor

def move_rule_up(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_up()
    return HttpResponseRedirect(reverse('admin:iprestrict_rule_changelist'))

def move_rule_down(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_down()
    return HttpResponseRedirect(reverse('admin:iprestrict_rule_changelist'))

def reload_rules(request):
    models.ReloadRulesRequest.request_reload()
    return HttpResponse('ok')
