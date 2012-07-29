from django.core.management.base import BaseCommand
from iprestrict import models

class Command(BaseCommand):
    help = 'Reloads the ip restriction rules from the DB'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', '1'))
        
        models.ReloadRulesRequest.request_reload()
        if verbosity >= 1:
            self.stdout.write('Successfully reloaded rules\n')
