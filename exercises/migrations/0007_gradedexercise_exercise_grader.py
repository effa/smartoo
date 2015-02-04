# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0006_auto_20150204_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradedexercise',
            name='exercise_grader',
            field=models.ForeignKey(default=None, to='exercises.ExercisesGrader'),
            preserve_default=False,
        ),
    ]
