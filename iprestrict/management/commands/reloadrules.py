from django.core.management.base import BaseCommand
from ... import models
from ...middleware import get_reload_rules_setting


class Command(BaseCommand):
    help = 'Requests the reload of the ip restriction rules from the DB.'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', '1'))

        reload_rules = get_reload_rules_setting()
        if not reload_rules:
            self.stderr.write("IPRESTRICT_RELOAD_RULES is set to False. "
                    "Your IPRestrict rules can't be changed dynamically.")
            return

        models.ReloadRulesRequest.request_reload()
        if verbosity >= 1:
            self.stdout.write('Successfully requested reload of rules\n')
