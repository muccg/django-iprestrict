# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

from ... import models


class Command(BaseCommand):
    help = 'Replaces the current rules in the DB with the rules in the given fixture file(s).'

    def add_arguments(self, parser):
        parser.add_argument('fixture', nargs='+')

    def handle(self, *args, **options):
        fixtures = options.get('fixture', [])

        with transaction.atomic():
            self.delete_existing_rules()
            call_command('loaddata', *fixtures, **options)

    def delete_existing_rules(self):
        models.Rule.objects.all().delete()
        models.IPRange.objects.all().delete()
        models.IPGroup.objects.all().delete()
