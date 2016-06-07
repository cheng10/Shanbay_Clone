from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_api.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions
from words.models import Learner, Word, VocaBook, KnownWords, LearningWords
from serializers import UserSerializer, GroupSerializer, LearnerSerializer, WordSerializer, \
    BookSerializer, KnownWordsSerializer, LearningWordsSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LearnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = VocaBook.objects.all()
    serializer_class = BookSerializer


class KnowWordsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = KnownWords.objects.all()
    serializer_class = KnownWordsSerializer


# class LevelWordViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = LevelWord.objects.all()
#     serializer_class = LevelWordSerializer


class LearningWordsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = LearningWords.objects.all()
    serializer_class = LearningWordsSerializer

    def perform_create(self, serializer):
        serializer.save(learner=Learner.objects.get(user=self.request.user))
