# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_auto_20150201_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practicer',
            name='behavior',
        ),
        migrations.AddField(
            model_name='practicer',
            name='behavior_name',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
