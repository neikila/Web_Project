# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pr', '0006_auto_20150120_0213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voteforposts',
            old_name='Type',
            new_name='p_type',
        ),
    ]
