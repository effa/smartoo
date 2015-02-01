# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercisescreator',
            old_name='name',
            new_name='behavior',
        ),
        migrations.RemoveField(
            model_name='exercisesgrader',
            name='name',
        ),
        migrations.AddField(
            model_name='exercisesgrader',
            name='behavior',
            field=models.CharField(default='blablabla', max_length=50),
            preserve_default=False,
        ),
    ]
