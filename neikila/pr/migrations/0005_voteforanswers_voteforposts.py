# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pr', '0004_profile_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteForAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('ans', models.ForeignKey(related_name=b'VoteForAnswer', to='pr.Answer')),
                ('voter', models.ForeignKey(related_name=b'VoteForAnswer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteForPosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('post', models.ForeignKey(related_name=b'VoteForPost', to='pr.Question')),
                ('voter', models.ForeignKey(related_name=b'VoteForPost', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
