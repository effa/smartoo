# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0006_auto_20150203_1223'),
        ('exercises', '0004_auto_20150202_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='options',
            name='exercise',
        ),
        migrations.DeleteModel(
            name='Options',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='knowledge_builder',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='question',
        ),
        migrations.AddField(
            model_name='exercise',
            name='data',
            field=common.fields.DictField(default=dict),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='knowledge_graph',
            field=models.ForeignKey(default=None, to='knowledge.KnowledgeGraph'),
            preserve_default=False,
        ),
    ]
