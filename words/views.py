from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse
from words.models import Word
from datetime import datetime


# Create your views here.
def home(request):
    word_list = Word.objects.all()
    return render(request, 'home.html', {'word_list': word_list})


def words(request):
    word_list = Word.objects.all()
    return render(request, 'words.html', {'word_list': word_list})


def word_detail(request, word_name):
    try:
        word = Word.objects.get(text=word_name)
    except Word.DoesNotExist:
        raise Http404()
    return render(request, 'word.html', {'word': word})


# def detail(request, id):
#     try:
#         word = Word.objects.get(id=str(id))
#     except Word.DoesNotExist:
#         raise Http404()
#     return render(request, 'word.html', {'word': word})


def test(request):
    return render(request, 'test.html', {'current_time': datetime.now()})
