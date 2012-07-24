from iprestrict import models

class IPRestrictor(object):
    def __init__(self):
        self.load_rules()


    # TODO I don't really like this method of reloading
    # Review
    @classmethod
    def get_instance(self):
        if not hasattr(self, '_instance'):
            self._instance = IPRestrictor()
        return self._instance

    def is_restricted(self, url, ip):
        for rule in self.rules:
            if rule.matches_url(url) and rule.matches_ip(ip):
                return rule.is_restricted()
        return False

    def load_rules(self):
        # We are caching the rules, to avoid DB lookup on each request
        self.rules = [r for r in models.Rule.objects.all()]

    reload_rules = load_rules
