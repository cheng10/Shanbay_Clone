# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_auto_20160603_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='note',
            field=models.ForeignKey(blank=True, to='words.Note', null=True),
        ),
    ]
