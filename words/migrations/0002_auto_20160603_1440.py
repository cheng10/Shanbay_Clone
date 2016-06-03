# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='vocab_book',
            field=models.ForeignKey(to='words.VocaBook', blank=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='note',
            field=models.ForeignKey(to='words.Note', blank=True),
        ),
    ]
