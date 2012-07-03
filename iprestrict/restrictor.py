from iprestrict import models

class IPRestrictor(object):
    def __init__(self):
        # We are caching the rules, to avoid DB lookup on each request
        self.rules = [r for r in models.Rule.objects.all()]

    def is_restricted(self, url, ip):
        for rule in self.rules:
            if rule.matches_url(url) and rule.matches_ip(ip):
                return rule.is_restricted()
        return False
