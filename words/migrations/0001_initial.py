# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KnownWords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['learner'],
            },
        ),
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('words_perday', models.PositiveIntegerField(default=0)),
                ('words_finished', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='LearningWords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('learner', models.ForeignKey(to='words.Learner')),
            ],
            options={
                'ordering': ['learner'],
            },
        ),
        migrations.CreateModel(
            name='LevelWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveSmallIntegerField(default=0, choices=[(0, 'none'), (1, 'a little'), (2, 'intermediate'), (3, 'advanced')])),
                ('learner', models.ForeignKey(to='words.Learner', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(to='words.Learner')),
            ],
            options={
                'ordering': ['word'],
            },
        ),
        migrations.CreateModel(
            name='VocaBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookname', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['bookname'],
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('desc', models.TextField()),
                ('sentence', models.TextField()),
            ],
            options={
                'ordering': ['text'],
            },
        ),
        migrations.AddField(
            model_name='vocabook',
            name='word',
            field=models.ManyToManyField(to='words.Word', blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='word',
            field=models.ForeignKey(related_name='word', to='words.Word'),
        ),
        migrations.AddField(
            model_name='levelword',
            name='word',
            field=models.ForeignKey(to='words.Word'),
        ),
        migrations.AddField(
            model_name='learningwords',
            name='word',
            field=models.ManyToManyField(to='words.LevelWord'),
        ),
        migrations.AddField(
            model_name='learner',
            name='vocab_book',
            field=models.ForeignKey(to='words.VocaBook', blank=True),
        ),
        migrations.AddField(
            model_name='knownwords',
            name='learner',
            field=models.ForeignKey(to='words.Learner'),
        ),
        migrations.AddField(
            model_name='knownwords',
            name='word',
            field=models.ManyToManyField(to='words.Word'),
        ),
    ]
