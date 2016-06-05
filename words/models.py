from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vocab_book = models.ForeignKey('VocaBook', on_delete=models.CASCADE, blank=True)
    words_perday = models.PositiveIntegerField(default=0)
    words_finished = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user']


class Word(models.Model):
    text = models.CharField(max_length=200)
    desc = models.TextField()
    sentence = models.TextField()

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id': self.id})
        return "localhost:8080%s" % path

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['text']


class Note(models.Model):
    word = models.ForeignKey('Word', related_name='word', on_delete=models.CASCADE)
    author = models.ForeignKey('Learner', on_delete=models.CASCADE)
    text = models.TextField()

    def __unicode__(self):
        return self.word.text+'_'+self.author.user.username

    class Meta:
        ordering = ['word']


class VocaBook(models.Model):
    bookname = models.CharField(max_length=200)
    word = models.ManyToManyField('Word', blank=True)

    def __unicode__(self):
        return self.bookname

    class Meta:
        ordering = ['bookname']


class KnownWords(models.Model):
    learner = models.ForeignKey('Learner', on_delete=models.CASCADE)
    word = models.ManyToManyField('Word')

    def __unicode__(self):
        return self.learner.user.username

    class Meta:
        ordering = ['learner']


class LevelWord(models.Model):
    MASTERY_LEVEL = (
        (0, 'none'),
        (1, 'a little'),
        (2, 'intermediate'),
        (3, 'advanced')
    )
    learner = models.ForeignKey('Learner', null=True, on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=MASTERY_LEVEL, default=0)

    def __unicode__(self):
        return self.learner.user.username+'_'+self.word.text


class LearningWords(models.Model):

    learner = models.ForeignKey('Learner', on_delete=models.CASCADE)
    word = models.ManyToManyField('LevelWord')

    def __unicode__(self):
        return self.learner.user.username

    class Meta:
        ordering = ['learner']
