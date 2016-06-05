# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0010_remove_levelword_learner'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelword',
            name='learner',
            field=models.ForeignKey(to='words.Learner', null=True),
        ),
    ]
