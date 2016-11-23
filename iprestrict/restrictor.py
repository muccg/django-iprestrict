# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone


class IPRestrictor(object):
    rules = None
    last_reload = None

    def __init__(self):
        self.load_rules()

    def is_restricted(self, url, ip):
        for rule in self.rules:
            if rule.matches_url(url) and rule.matches_ip(ip):
                return rule.is_restricted()
        return False

    def load_rules(self):
        # We are caching the rules, to avoid DB lookup on each request
        from .models import Rule
        self.rules = list(Rule.objects.all())
        self.last_reload = timezone.now()

    reload_rules = load_rules
