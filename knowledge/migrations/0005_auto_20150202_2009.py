# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import knowledge.fields


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0004_auto_20150202_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledgegraph',
            name='serialized_graph',
        ),
        migrations.AddField(
            model_name='knowledgegraph',
            name='graph',
            field=knowledge.fields.GraphField(default=None),
            preserve_default=False,
        ),
    ]
