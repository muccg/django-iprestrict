from django.core.management.base import BaseCommand
from ... import models


class Command(BaseCommand):
    help = 'Requests the reload of the ip restriction rules from the DB.'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', '1'))

        models.ReloadRulesRequest.request_reload()
        if verbosity >= 1:
            self.stdout.write('Successfully requested reload of rules\n')
