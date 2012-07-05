from django.http import HttpResponseRedirect
from iprestrict import models

def move_rule_up(request, rule_id):
    print "ouch " + rule_id
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_up()
    return HttpResponseRedirect('/admin/iprestrict/rule')

def move_rule_down(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_down()
    return HttpResponseRedirect('/admin/iprestrict/rule')
