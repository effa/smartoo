# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code_path', models.TextField()),
                ('parameters', models.TextField()),
                ('performance', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
