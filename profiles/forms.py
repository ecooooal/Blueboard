from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }
        widgets = {
            'profile_picture': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 3 })
        }