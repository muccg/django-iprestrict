# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iprestrict', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationBasedIPGroup',
            fields=[
            ],
            options={
                'verbose_name': 'Location Based IP Group',
                'proxy': True,
            },
            bases=('iprestrict.ipgroup',),
        ),
        migrations.CreateModel(
            name='RangeBasedIPGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('iprestrict.ipgroup',),
        ),
        migrations.AddField(
            model_name='ipgroup',
            name='type',
            field=models.CharField(default='range', max_length=10, choices=[('location', 'location based'), ('range', 'range based')]),
        ),
    ]
