# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0005_auto_20160604_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knownwords',
            name='word',
        ),
        migrations.AddField(
            model_name='knownwords',
            name='word',
            field=models.ManyToManyField(to='words.Word'),
        ),
        migrations.RemoveField(
            model_name='learningwords',
            name='word',
        ),
        migrations.AddField(
            model_name='learningwords',
            name='word',
            field=models.ManyToManyField(to='words.Word'),
        ),
        migrations.RemoveField(
            model_name='vocabook',
            name='word',
        ),
        migrations.AddField(
            model_name='vocabook',
            name='word',
            field=models.ManyToManyField(to='words.Word'),
        ),
    ]
