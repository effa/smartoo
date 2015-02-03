# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import knowledge.models
import knowledge.fields


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0005_auto_20150202_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledgegraph',
            name='graph',
            field=knowledge.fields.GraphField(default=knowledge.models.get_initialized_graph),
            preserve_default=True,
        ),
    ]
