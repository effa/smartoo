# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartoo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='topic',
        ),
        migrations.AddField(
            model_name='session',
            name='topic_uri',
            field=models.CharField(default=None, max_length=120),
            preserve_default=False,
        ),
    ]
