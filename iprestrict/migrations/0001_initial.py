# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'IP Group',
            },
        ),
        migrations.CreateModel(
            name='IPRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_ip', models.GenericIPAddressField()),
                ('cidr_prefix_length', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('last_ip', models.GenericIPAddressField(null=True, blank=True)),
                ('ip_group', models.ForeignKey(to='iprestrict.IPGroup')),
            ],
            options={
                'verbose_name': 'IP Range',
            },
        ),
        migrations.CreateModel(
            name='ReloadRulesRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_pattern', models.CharField(max_length=500)),
                ('action', models.CharField(default=b'D', max_length=1, choices=[(b'A', b'ALLOW'), (b'D', b'DENY')])),
                ('rank', models.IntegerField(blank=True)),
                ('ip_group', models.ForeignKey(default=1, to='iprestrict.IPGroup')),
            ],
            options={
                'ordering': ['rank', 'id'],
            },
        ),
    ]
