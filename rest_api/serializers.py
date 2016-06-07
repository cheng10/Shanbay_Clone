from django.contrib.auth.models import User, Group
from rest_framework import serializers
from words.models import Learner, Word, VocaBook, KnownWords, LearningWords


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class LearnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Learner
        fields = ('url', 'user', 'vocab_book', 'words_perday', 'words_finished')


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('url', 'text', 'desc', 'sentence')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VocaBook
        fields = ('url', 'bookname', 'word')


class KnownWordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KnownWords
        fields = ('url', 'learner', 'word')


# class LevelWordSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = LevelWord
#         fields = ('url', 'word', 'level')


class LearningWordsSerializer(serializers.HyperlinkedModelSerializer):
    learner = serializers.ReadOnlyField(source='learner.user.username')

    class Meta:
        model = LearningWords
        fields = ('url', 'learner', 'word')
