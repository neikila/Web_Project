# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pr', '0002_auto_20150116_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_text',
            field=models.CharField(max_length=30),
        ),
    ]
