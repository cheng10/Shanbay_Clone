from __future__ import print_function

import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from words.models import Word, Learner, VocaBook, LearningWords
from forms import UserForm, LearnerForm
from datetime import datetime
import json


# Create your views here.
def home(request):
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
    word_list = Word.objects.all()
    return render(request, 'words.html', {'word_list': word_list})


@login_required()
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

@login_required()
def bdc(request):
    # redirect admin to admin page
    try:
        learner = Learner.objects.get(user=request.user)
    except Learner.DoesNotExist:
        return HttpResponseRedirect('/admin')
    else:
        # learning word list initial set up
        try:
            l = LearningWords.objects.get(learner=learner)
        except LearningWords.DoesNotExist:
            l = LearningWords.objects.create(learner=learner)
            for word in learner.vocab_book.word.all():
                l.word.add(word)
            l.save()
        wordlist = l.word.all()
        word = wordlist[0]
        return render(request, 'bdc.html', {'learner': learner, 'word': word})


@login_required()
def bdc_know(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            learner_id = json_data['learnerId']
            word_name = json_data['wordName']
            learner = Learner.objects.get(id=learner_id)
            words = LearningWords.objects.get(learner=learner)
            word = Word.objects.get(text=word_name)
            words.word.remove(word)
            words.save()

    return HttpResponse("OK")


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
            print (user_form.errors, learner_form.errors)

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
