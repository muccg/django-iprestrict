# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iprestrict', '0004_add_iplocation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ipgroup',
            options={'verbose_name': 'IP Group'},
        ),
        migrations.AddField(
            model_name='rule',
            name='reverse_ip_group',
            field=models.BooleanField(default=False),
        ),
    ]
