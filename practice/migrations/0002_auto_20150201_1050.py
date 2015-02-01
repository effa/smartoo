# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practicer',
            name='name',
        ),
        migrations.AddField(
            model_name='practicer',
            name='behavior',
            field=models.CharField(default='bla', max_length=50),
            preserve_default=False,
        ),
    ]
