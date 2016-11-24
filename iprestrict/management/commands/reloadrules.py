# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ._utils import warn_about_renamed_command
from . import reload_rules


class Command(reload_rules.Command):

    def handle(self, *args, **options):
        warn_about_renamed_command('reloadrules', 'reload_rules')
        super(Command, self).handle(*args, **options)
