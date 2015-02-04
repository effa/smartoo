# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0007_gradedexercise_exercise_grader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradedexercise',
            name='exercise_grader',
        ),
        migrations.AddField(
            model_name='gradedexercise',
            name='exercises_grader',
            field=models.ForeignKey(default=None, to='exercises.ExercisesGrader'),
            preserve_default=False,
        ),
    ]
