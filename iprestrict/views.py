# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import json

from . import models
from .decorators import superuser_required


@superuser_required
def move_rule_up(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_up()
    return HttpResponseRedirect(reverse('admin:iprestrict_rule_changelist'))


@superuser_required
def move_rule_down(request, rule_id):
    rule = models.Rule.objects.get(pk=rule_id)
    rule.move_down()
    return HttpResponseRedirect(reverse('admin:iprestrict_rule_changelist'))


@superuser_required
def reload_rules(request):
    models.ReloadRulesRequest.request_reload()
    return HttpResponse('ok')


@superuser_required
def test_rules_page(request):
    return render_to_response('iprestrict/test_rules.html')


@superuser_required
def test_match(request):
    request_dict = request.GET
    if request.method == 'POST':
        request_dict = request.POST
    url = request_dict['url']
    ip = request_dict['ip']

    matching_rule_id, action = find_matching_rule(url, ip)
    rules = list_rules(matching_rule_id, url, ip)

    if matching_rule_id is None:
        result = {
            'action': 'Allowed',
            'msg': 'No rules matched.',
        }
    else:
        result = {
            'action': action,
            'msg': 'URL matched Rule highlighted below.'
        }
    result['rules'] = rules

    return HttpResponse(json.dumps(result))


def find_matching_rule(url, ip):
    for r in models.Rule.objects.all():
        if r.matches_url(url) and r.matches_ip(ip):
            return r.pk, r.action_str()
    return None, None


def list_rules(matching_rule_id, url, ip):
    return [map_rule(r, matching_rule_id, url, ip) for r in models.Rule.objects.all()]


def map_rule(r, matching_rule_id, url, ip):
    rule = {
        'url_pattern': {
            'value': r.url_pattern,
            'matchStatus': 'match' if r.matches_url(url) else 'noMatch'
        },
        'ip_group': {
            'name': r.ip_group.name,
            'reverse_ip_group': 'NOT' if r.reverse_ip_group else '',
            'ranges': r.ip_group.details_str(),
            'matchStatus': 'match' if r.matches_ip(ip) else 'noMatch'
        },
        'action': r.action_str(),
    }
    if r.pk == matching_rule_id:
        rule['matched'] = True
    return rule
