# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.core.management import call_command

from ... import models


class Command(BaseCommand):
    help = 'Replaces the current rules in the DB with the rules in the given fixture file(s).'
    args = "fixture [fixture ...]"

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', '1'))

        self.delete_existing_rules()
        if verbosity >= 1:
            self.stdout.write('Successfully deleted rules')

        call_command('loaddata', *args, verbosity=verbosity, interactive=False)

    def delete_existing_rules(self):
        models.Rule.objects.all().delete()
        models.IPRange.objects.all().delete()
        models.IPGroup.objects.all().delete()
