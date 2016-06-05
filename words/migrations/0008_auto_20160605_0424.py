# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0007_auto_20160605_0402'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveSmallIntegerField(default=0, choices=[(0, 'none'), (1, 'a little'), (2, 'intermediate'), (3, 'advanced')])),
                ('word', models.ForeignKey(to='words.Word')),
            ],
        ),
        migrations.RemoveField(
            model_name='learningwords',
            name='level',
        ),
        migrations.AlterField(
            model_name='learningwords',
            name='word',
            field=models.ManyToManyField(to='words.LevelWord'),
        ),
        migrations.DeleteModel(
            name='Level',
        ),
    ]
