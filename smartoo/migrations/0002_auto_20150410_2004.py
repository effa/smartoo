# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import knowledge.fields


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_practicer'),
        ('knowledge', '0002_auto_20150410_2004'),
        ('exercises', '0002_auto_20150410_2004'),
        ('smartoo', '0001_initial'),
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
                ('final_rating', models.FloatField(default=0.5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackedExercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answered', models.BooleanField(default=False)),
                ('correct', models.BooleanField(default=False)),
                ('invalid', models.BooleanField(default=False)),
                ('irrelevant', models.BooleanField(default=False)),
                ('exercise', models.ForeignKey(to='exercises.Exercise')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', knowledge.fields.TermField()),
                ('start', models.DateTimeField()),
                ('finnished', models.BooleanField(default=False)),
                ('exercises_creator', models.ForeignKey(to='exercises.ExercisesCreator')),
                ('exercises_grader', models.ForeignKey(to='exercises.ExercisesGrader')),
                ('feedback', models.OneToOneField(to='smartoo.AccumulativeFeedback')),
                ('knowledge_builder', models.ForeignKey(to='knowledge.KnowledgeBuilder')),
                ('practicer', models.ForeignKey(to='practice.Practicer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='feedbackedexercise',
            name='session',
            field=models.ForeignKey(to='smartoo.Session'),
            preserve_default=True,
        ),
    ]
