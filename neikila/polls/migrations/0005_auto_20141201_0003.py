# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_question_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='author_id',
            new_name='author',
        ),
    ]
