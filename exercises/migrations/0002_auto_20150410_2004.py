# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0002_auto_20150410_2004'),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', common.fields.DictField(default=dict)),
                ('semantics', common.fields.DictField(default=dict)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExercisesCreator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('behavior_name', models.CharField(max_length=50)),
                ('parameters', common.fields.DictField(default=dict, null=True, blank=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExercisesGrader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('behavior_name', models.CharField(max_length=50)),
                ('parameters', common.fields.DictField(default=dict, null=True, blank=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GradedExercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField()),
                ('correctness', models.FloatField()),
                ('relevance', models.FloatField()),
                ('exercise', models.ForeignKey(to='exercises.Exercise')),
                ('exercises_grader', models.ForeignKey(to='exercises.ExercisesGrader')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercises_creator',
            field=models.ForeignKey(to='exercises.ExercisesCreator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='knowledge_graph',
            field=models.ForeignKey(to='knowledge.KnowledgeGraph'),
            preserve_default=True,
        ),
    ]
