# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20141201_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagForAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='polls.Answer')),
                ('tag', models.ForeignKey(to='polls.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagForQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.ForeignKey(to='polls.Question')),
                ('tag', models.ForeignKey(to='polls.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(default=1, to='polls.User'),
        ),
    ]
