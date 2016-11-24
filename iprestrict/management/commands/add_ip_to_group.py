# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_ipv46_address
from ... import models


class Command(BaseCommand):
    help = 'Adds an IP address to an IP Group.'

    def add_arguments(self, parser):
        parser.add_argument('group_name')
        parser.add_argument('ip', nargs='+')

    def handle(self, *args, **options):
        group_name = options.get('group_name')
        ips = options.get('ip')

        try:
            ip_group = models.IPGroup.objects.get(name__iexact=group_name, type=models.TYPE_RANGE)
        except models.IPGroup.DoesNotExist:
            try:
                models.IPGroup.objects.get(name__iexact=group_name)
            except models.IPGroup.DoesNotExist:
                raise CommandError("IPGroup '%s' doesn't exist." % group_name)
            else:
                raise CommandError("Can add IP address only to a Range based IP Group.")

        for ip in ips:
            try:
                validate_ipv46_address(ip)
            except ValidationError:
                raise CommandError("'%s' not a valid IPv4 or IPv6 address." % ip)

        for ip in ips:
            models.IPRange.objects.get_or_create(ip_group=ip_group, first_ip=ip)
