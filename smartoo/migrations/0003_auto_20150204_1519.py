# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0007_gradedexercise_exercise_grader'),
        ('smartoo', '0002_exercisefeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccumulativeFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correct_count', models.SmallIntegerField(default=0)),
                ('wrong_count', models.SmallIntegerField(default=0)),
                ('unanswered_count', models.SmallIntegerField(default=0)),
                ('invalid_count', models.SmallIntegerField(default=0)),
                ('irrelevant_count', models.SmallIntegerField(default=0)),
                ('quality', models.FloatField(default=None, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackedExercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answered', models.BooleanField(default=True)),
                ('correct', models.BooleanField(default=False)),
                ('invalid', models.BooleanField(default=False)),
                ('irrelevant', models.BooleanField(default=False)),
                ('graded_exercise', models.ForeignKey(to='exercises.GradedExercise')),
                ('session', models.ForeignKey(to='smartoo.Session')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='exercisefeedback',
            name='exercise',
        ),
        migrations.RemoveField(
            model_name='exercisefeedback',
            name='session',
        ),
        migrations.DeleteModel(
            name='ExerciseFeedback',
        ),
        migrations.RemoveField(
            model_name='session',
            name='correct_count',
        ),
        migrations.RemoveField(
            model_name='session',
            name='invalid_count',
        ),
        migrations.RemoveField(
            model_name='session',
            name='irrelevant_count',
        ),
        migrations.RemoveField(
            model_name='session',
            name='quality',
        ),
        migrations.RemoveField(
            model_name='session',
            name='unanswered_count',
        ),
        migrations.RemoveField(
            model_name='session',
            name='wrong_count',
        ),
        migrations.AddField(
            model_name='session',
            name='feedback',
            field=models.OneToOneField(default=None, to='smartoo.AccumulativeFeedback'),
            preserve_default=False,
        ),
    ]
