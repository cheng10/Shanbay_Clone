from django import forms
from django.contrib.auth.models import User
from models import Learner


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LearnerForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('vocab_book', 'words_perday')
