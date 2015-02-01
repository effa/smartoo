# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledgebuilder',
            name='name',
        ),
        migrations.AddField(
            model_name='knowledgebuilder',
            name='behavior',
            field=models.CharField(default='bla', max_length=50),
            preserve_default=False,
        ),
    ]
