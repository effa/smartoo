# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_auto_20150203_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradedExercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField()),
                ('correctness', models.FloatField()),
                ('relevance', models.FloatField()),
                ('exercise', models.ForeignKey(to='exercises.Exercise')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='exercisegrades',
            name='exercise',
        ),
        migrations.DeleteModel(
            name='ExerciseGrades',
        ),
    ]
