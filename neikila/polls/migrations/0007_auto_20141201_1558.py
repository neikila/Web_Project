# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20141201_0550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagforanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='tagforanswer',
            name='tag',
        ),
        migrations.DeleteModel(
            name='TagForAnswer',
        ),
    ]
