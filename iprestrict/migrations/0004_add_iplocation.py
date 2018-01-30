# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iprestrict', '0003_add_ipgroup_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_codes', models.CharField(help_text='Comma-separated list of 2 character country codes', max_length=2000)),
            ],
            options={
                'verbose_name': 'IP Location',
            },
        ),
        migrations.AlterModelOptions(
            name='ipgroup',
            options={},
        ),
        migrations.AlterModelOptions(
            name='rangebasedipgroup',
            options={'verbose_name': 'IP Group'},
        ),
        migrations.AlterField(
            model_name='ipgroup',
            name='type',
            field=models.CharField(default='range', max_length=10, choices=[('location', 'Location based'), ('range', 'Range based')]),
        ),
        migrations.AddField(
            model_name='iplocation',
            name='ip_group',
            field=models.ForeignKey(to='iprestrict.IPGroup', on_delete=models.CASCADE),
        ),
    ]
