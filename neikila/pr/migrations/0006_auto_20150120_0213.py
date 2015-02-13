# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pr', '0005_voteforanswers_voteforposts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voteforanswers',
            name='ans',
        ),
        migrations.RemoveField(
            model_name='voteforanswers',
            name='voter',
        ),
        migrations.DeleteModel(
            name='VoteForAnswers',
        ),
        migrations.AddField(
            model_name='voteforposts',
            name='Type',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
