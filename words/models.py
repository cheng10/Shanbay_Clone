from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vocab_book = models.ForeignKey('VocaBook', on_delete=models.CASCADE, blank=True)
    words_perday = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class Word(models.Model):
    text = models.CharField(max_length=200)
    desc = models.TextField()
    sentence = models.TextField()
    note = models.ForeignKey('Note', on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return self.text


class Note(models.Model):
    author = models.ForeignKey('Learner', on_delete=models.CASCADE)
    text = models.TextField()

    def __unicode__(self):
        return self.text


class VocaBook(models.Model):
    bookname = models.CharField(max_length=200)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.bookname

class KnownWords(models.Model):
    learner = models.ForeignKey('Learner', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)


class LearningWords(models.Model):
    MASTERY_LEVEL = (
        (0, 'none'),
        (1, 'a little'),
        (2, 'intermediate'),
        (3, 'advanced')
    )
    learner = models.ForeignKey('Learner', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=MASTERY_LEVEL, default=0)
