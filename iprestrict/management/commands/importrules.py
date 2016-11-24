# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._utils import warn_about_renamed_command
from . import import_rules


class Command(import_rules.Command):

    def handle(self, *args, **options):
        warn_about_renamed_command('importrules', 'import_rules')
        super(Command, self).handle(*args, **options)
