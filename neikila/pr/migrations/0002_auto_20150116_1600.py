# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='question',
            field=models.ManyToManyField(to='pr.Question'),
            preserve_default=True,
        ),
    ]
