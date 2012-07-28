from django.core.management.base import BaseCommand
from iprestrict import models

class Command(BaseCommand):
    help = 'Reloads the ip restriction rules from the DB'

    def handle(self, *args, **options):
        models.ReloadRulesRequest.request_reload()
        self.stdout.write('Successfully reloaded rules\n')
