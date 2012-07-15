from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from iprestrict import models

def move_rule_up(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_up()
    return HttpResponseRedirect(reverse('admin:iprestrict_rule_changelist'))

def move_rule_down(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_down()
    return HttpResponseRedirect(reverse('admin:iprestrict_rule_changelist'))
