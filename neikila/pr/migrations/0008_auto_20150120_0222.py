# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pr', '0007_auto_20150120_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteforposts',
            name='post',
            field=models.IntegerField(default=0),
        ),
    ]
