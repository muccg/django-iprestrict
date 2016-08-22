# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_data(apps, schema_editor):
    IPGroup = apps.get_model('iprestrict', 'IPGroup')
    IPRange = apps.get_model("iprestrict", "IPRange")
    Rule = apps.get_model("iprestrict", "Rule")

    # Default IP Groups: ALL and localhost
    all_group = IPGroup.objects.create(
        name='ALL',
        description='Matches all IP Addresses')
    localhost_group = IPGroup.objects.create(
        name='localhost',
        description='IP address of localhost')

    # IP ranges defining ALL and localhost for ipv4 and ipv6
    IPRange.objects.create(
        ip_group=all_group,
        first_ip='0.0.0.0',
        last_ip='255.255.255.255')
    IPRange.objects.create(
        ip_group=all_group,
        first_ip='0:0:0:0:0:0:0:0',
        last_ip='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')
    IPRange.objects.create(
        ip_group=localhost_group,
        first_ip='127.0.0.1',
        last_ip=None)
    IPRange.objects.create(
        ip_group=localhost_group,
        first_ip='::1',
        last_ip=None)

    # Default rules: Allow all for localhost and Deny everything else
    Rule.objects.create(
        ip_group=localhost_group,
        action='A',
        url_pattern='ALL',
        rank=65535)
    Rule.objects.create(
        ip_group=all_group,
        action='D',
        url_pattern='ALL',
        rank=65536)


class Migration(migrations.Migration):

    dependencies = [
        ('iprestrict', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
