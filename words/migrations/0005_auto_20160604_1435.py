# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_auto_20160604_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ['text']},
        ),
    ]
