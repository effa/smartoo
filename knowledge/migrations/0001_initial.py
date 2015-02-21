# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import knowledge.models
import common.fields
import knowledge.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('behavior_name', models.CharField(max_length=50)),
                ('parameters', common.fields.DictField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KnowledgeGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', knowledge.fields.TermField()),
                ('graph', knowledge.fields.GraphField(default=knowledge.models.get_initialized_graph)),
                ('knowledge_builder', models.ForeignKey(to='knowledge.KnowledgeBuilder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vertical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', knowledge.fields.TermField(unique=True)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
