from __future__ import print_function

import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from words.models import Word, Learner, VocaBook, LearningWords, ReviewWords, KnownWords
from forms import UserForm, LearnerForm
from datetime import datetime
import json
import random


# Create your views here.
def home(request):
    # print('home')
    # restrict access
    if request.user.is_authenticated():
        # redirect admin to admin page
        try:
            learner = Learner.objects.get(user=request.user)
        except Learner.DoesNotExist:
            return HttpResponseRedirect('/admin')
        else:
            word_list = Word.objects.all()
            return render(request, 'home.html', {'word_list': word_list, 'learner': learner})
    else:
        word_list = Word.objects.all()
        return render(request, 'home.html', {'word_list': word_list})


@login_required()
def words(request):
    # print('words')
    word_list = Word.objects.all()
    return render(request, 'words.html', {'word_list': word_list})


@login_required()
def word_detail(request, word_name):
    try:
        word = Word.objects.get(text=word_name)
    except Word.DoesNotExist:
        raise Http404()
    return render(request, 'word.html', {'word': word})


@login_required()
def word_like(request):
    # print('word_like')
    word_id = None
    if request.method == "GET":
        word_id = request.GET['word_id']
    likes = 0
    if word_id:
        word = Word.objects.get(id=int(word_id))
        if word:
            likes = word.likes + 1
            # print('word_like, ', likes)
            word.likes = likes
            word.save()
    return HttpResponse(likes)


def get_word_list(max_results=0, starts_with=''):
    word_list = []
    if starts_with:
        word_list = Word.objects.filter(text__istartswith=starts_with)
    if starts_with == '':
        word_list = Word.objects.all()
    if max_results > 0:
        if word_list.count > max_results:
            word_list = word_list[:max_results]
    return word_list


def suggest_word(request):
    word_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    word_list = get_word_list(8, starts_with)
    # if nothing in the search box, return all words
    if starts_with == '':
        word_list = get_word_list(0, starts_with)
    return render(request, 'suggest_word.html', {'word_list': word_list})


@login_required()
def bdc(request):
    # print('bdc')
    message = ''
    # redirect admin to admin page
    try:
        learner = Learner.objects.get(user=request.user)
    except Learner.DoesNotExist:
        return HttpResponseRedirect('/admin')
    else:
        # if learner did not log in within one day, reset the words_finished to 0
        last_login = request.user.last_login.isoformat().split('T')[0]
        now = datetime.now().isoformat().split('T')[0]
        # print (last_login, now)
        if last_login != now:
            learner.words_finished = 0
            learner.save()
        # learning word list initial set up
        KnownWords.objects.get_or_create(learner=learner)
        ReviewWords.objects.get_or_create(learner=learner)
        try:
            l = LearningWords.objects.get(learner=learner)
        except LearningWords.DoesNotExist:
            l = LearningWords.objects.create(learner=learner)
            for word in learner.vocab_book.word.all():
                l.word.add(word)
            l.save()
        wordlist = l.word.all().order_by('?')
        # if learner finished all the word in the book, just redirect him to home page
        print("words in the learning list: ", l.word.count())
        if l.word.count() <= 0:
            message = "You have finished all the words in the book. Good Job!"
            return render(request, 'home.html', {'learner': learner, "wordlist": wordlist, "message": message})
        # if learner finished all the word today, redirect him to home
        if learner.words_finished >= learner.words_perday:
            message = "You have finished all the words today. Good Job!"
            return render(request, 'home.html', {'learner': learner, "wordlist": wordlist, "message": message})
        return render(request, 'bdc.html', {'learner': learner, "wordlist": wordlist, "message": message,
                                            "learning_word_count": l.word.count()})


@login_required()
def bdc_know(request):
    # print('bdc_know')
    learner_id = None
    word_id = None
    if request.method == "GET":
        learner_id = request.GET['learner_id']
        word_id = request.GET['word_id']
    words_finished = 0
    word = None
    learning_words = None
    review_words = None
    known_words = None
    learner = None
    wordlist = None
    l = None
    if learner_id:
        learner = Learner.objects.get(id=int(learner_id))
        if learner:
            learning_words = LearningWords.objects.get(learner=learner)

            # if learner finished all the word in the book, just redirect him to home page
            l = learning_words
            print("words in the learning list: ", l.word.count())
            if l.word.count() <= 0:
                message = "You have finished all the words in the book. Good Job!"

            review_words = ReviewWords.objects.get(learner=learner)
            # known_words = KnownWords.objects.get(learner=learner)
            # print (known_words)
            words_finished = learner.words_finished + 1
            learner.words_finished = words_finished
            learner.save()
    if word_id:
        word = Word.objects.get(id=int(word_id))
        if word:
            if learning_words.word.filter(id=word.id).exists():
                print("know learningword")
                learning_words.word.remove(word)
                learning_words.save()
                wordlist = learning_words.word.all().order_by('?')
            elif review_words.word.filter(id=word.id).exists():
                print("know reviewword")
                review_words.word.remove(word)
                review_words.save()
                wordlist = review_words.word.all().order_by('?')
            print("remove word")
            # known_words.word.add(word)
            # print ("add known")
            # known_words.save()
            words_perday = learner.words_perday
            words_finished = learner.words_finished
            review_list = review_words.word.all().order_by('?')
            if review_words.word.count() >= (words_perday - words_finished):
                wordlist = review_list
    return render(request, 'bdc_update.html',
                  {'learner': learner, "wordlist": wordlist, "learning_word_count": l.word.count()})


@login_required()
def bdc_not_know(request):
    # print('bdc_know')
    learner_id = None
    word_id = None
    if request.method == "GET":
        learner_id = request.GET['learner_id']
        word_id = request.GET['word_id']
    words_finished = 0
    words_perday = 0
    word = None
    learning_words = None
    review_words = None
    learner = None
    wordlist = None
    if learner_id:
        learner = Learner.objects.get(id=int(learner_id))
        if learner:
            learning_words = LearningWords.objects.get(learner=learner)
            review_words = ReviewWords.objects.get(learner=learner)
            words_finished = learner.words_finished
            words_perday = learner.words_perday
    if word_id:
        word = Word.objects.get(id=int(word_id))
        if word:
            if learning_words.word.filter(id=word.id).exists():
                learning_words.word.remove(word)
                review_words.word.add(word)
                learning_words.save()
                review_words.save()
            # if no more learning_words, only review_words
            elif review_words.word.filter(id=word.id).exists():
                # try to avoid showing the same word when not_know being clicked
                review_list = review_words.word.all().order_by('?')
                wordlist = review_list
                print(review_words.word.count())
                print(words_perday)
                print(words_finished)
                return render(request, 'bdc_update.html', {'learner': learner, "wordlist": wordlist,})

            review_list = review_words.word.all().order_by('?')
            wordlist = learning_words.word.all().order_by('?')
            # if review_words reach today's max
            print(review_words.word.count())
            print(words_perday)
            print(words_finished)
            if review_words.word.count() >= (words_perday - words_finished):
                wordlist = review_list
    return render(request, 'bdc_update.html', {'learner': learner, "wordlist": wordlist,})


# @login_required()
# def bdc_know(request):
#     print('bdc_know')
#     # if request.is_ajax():
#     if request.method == 'POST':
#         json_data = json.loads(request.body)
#         learner_id = json_data['learnerId']
#         word_name = json_data['wordName']
#         learner = Learner.objects.get(id=learner_id)
#         words = LearningWords.objects.get(learner=learner)
#         word = Word.objects.get(text=word_name)
#         words.word.remove(word)
#         words.save()
#     return HttpResponse(200)


def about(request):
    return render(request, 'about.html', {'current_time': datetime.now()})


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        learner_form = LearnerForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and learner_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            learner = learner_form.save(commit=False)
            learner.user = user
            learner.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, learner_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        learner_form = LearnerForm()

    # Render the template depending on the context.
    return render(request,
                  'signup.html',
                  {'user_form': user_form, 'learner_form': learner_form, 'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                # return HttpResponse("Your account is disabled.")
                message = 'Your account is disabled.'
                return render(request,
                              'login.html',
                              {'message': message})

        else:
            # Bad login details were provided. So we can't log the user in.
            # print "Invalid login details: {0}, {1}".format(username, password)
            message = 'Invalid login details supplied.'
            return render(request,
                          'login.html',
                          {'message': message})
            # return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    # print "You have signed off"
    return render(request, 'home.html', {'message': 'You have signed off.'})
