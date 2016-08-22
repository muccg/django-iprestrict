# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_data(apps, schema_editor):
    IPGroup = apps.get_model('iprestrict', 'IPGroup')
    first_group = IPGroup.objects.create(
        name='ALL',
        description='Matches all IP Addresses')
    second_group = IPGroup.objects.create(
        name='localhost',
        description='IP address of localhost')

    IPRange = apps.get_model('iprestrict', 'IPRange')
    IPRange.objects.create(
        ip_group=first_group,
        first_ip='0.0.0.0',
        last_ip='255.255.255.255')
    IPRange.objects.create(
        ip_group=first_group,
        first_ip='0:0:0:0:0:0:0:0',
        last_ip='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')
    IPRange.objects.create(
        ip_group=second_group,
        first_ip='127.0.0.1',
        last_ip=None)
    IPRange.objects.create(
        ip_group=second_group,
        first_ip='::1',
        last_ip=None)

    Rule = apps.get_model('iprestrict', 'Rule')
    Rule.objects.create(
        ip_group=first_group,
        action='A',
        url_pattern='ALL',
        rank=65536)
    Rule.objects.create(
        ip_group=second_group,
        action='A',
        url_pattern='ALL',
        rank=65535)


class Migration(migrations.Migration):

    dependencies = [
        ('iprestrict', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]
