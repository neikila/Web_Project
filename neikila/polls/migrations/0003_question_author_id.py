# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='author_id',
            field=models.ForeignKey(default=1, to='polls.User'),
            preserve_default=True,
        ),
    ]
