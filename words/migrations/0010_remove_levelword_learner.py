# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0009_levelword_learner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='levelword',
            name='learner',
        ),
    ]
