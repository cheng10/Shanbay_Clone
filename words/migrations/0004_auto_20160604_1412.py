# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0003_auto_20160603_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ['-text']},
        ),
    ]
