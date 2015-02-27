# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartoo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
