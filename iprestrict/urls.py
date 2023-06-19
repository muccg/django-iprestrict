# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import re_path
from .views import test_rules_page, test_match, reload_rules
from .views import move_rule_up, move_rule_down

app_name = "iprestrict"
urlpatterns = [
    re_path(r'^$', test_rules_page),
    re_path(r'^move_rule_up/(?P<rule_id>\d+)[/]?$', move_rule_up, name='move_rule_up'),
    re_path(r'^move_rule_down/(?P<rule_id>\d+)[/]?$', move_rule_down, name='move_rule_down'),
    re_path(r'^reload_rules[/]?$', reload_rules, name='reload_rules'),
    re_path(r'^test_match[/]?$', test_match, name='test_match'),
]
