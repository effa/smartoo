# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartoo', '0002_auto_20150410_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackedexercise',
            name='exercise',
            field=models.ForeignKey(to='exercises.GradedExercise'),
            preserve_default=True,
        ),
    ]
