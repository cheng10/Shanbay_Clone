# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0006_auto_20160605_0344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveSmallIntegerField(default=0, choices=[(0, 'none'), (1, 'a little'), (2, 'intermediate'), (3, 'advanced')])),
            ],
        ),
        migrations.AlterModelOptions(
            name='knownwords',
            options={'ordering': ['learner']},
        ),
        migrations.AlterModelOptions(
            name='learner',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='learningwords',
            options={'ordering': ['learner']},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['author']},
        ),
        migrations.AlterModelOptions(
            name='vocabook',
            options={'ordering': ['bookname']},
        ),
        migrations.RemoveField(
            model_name='learningwords',
            name='level',
        ),
        migrations.AddField(
            model_name='learningwords',
            name='level',
            field=models.ManyToManyField(to='words.Level'),
        ),
    ]
