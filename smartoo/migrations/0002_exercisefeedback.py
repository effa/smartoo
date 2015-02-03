# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_auto_20150203_1223'),
        ('smartoo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answered', models.BooleanField(default=True)),
                ('correct', models.BooleanField(default=False)),
                ('invalid', models.BooleanField(default=False)),
                ('irrelevant', models.BooleanField(default=False)),
                ('exercise', models.ForeignKey(to='exercises.Exercise')),
                ('session', models.ForeignKey(to='smartoo.Session')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
