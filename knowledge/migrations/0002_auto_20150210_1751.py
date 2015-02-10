# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartoo', '0002_auto_20150210_1751'),
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='vertical',
        ),
        migrations.RemoveField(
            model_name='knowledgegraph',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.AddField(
            model_name='knowledgegraph',
            name='topic_uri',
            field=models.CharField(default=None, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vertical',
            name='topic_uri',
            field=models.CharField(default=None, unique=True, max_length=120),
            preserve_default=False,
        ),
    ]
