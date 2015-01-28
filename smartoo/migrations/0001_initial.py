# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correct_count', models.SmallIntegerField(default=0)),
                ('wrong_count', models.SmallIntegerField(default=0)),
                ('unanswered_count', models.SmallIntegerField(default=0)),
                ('mean_time', models.IntegerField()),
                ('invalid_count', models.SmallIntegerField(default=0)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('finnished', models.BooleanField(default=False)),
                ('knowledge_builder', models.ForeignKey(to='knowledge.KnowledgeBuilder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
