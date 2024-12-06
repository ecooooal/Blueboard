from django import forms
from django.forms import ModelForm
from .models import Kanban, KanbanMember, Column, Card

VISIBILITY_CHOICES = {True:'Public', False:'Private'}

class KanbanCreateForm(ModelForm):
    class Meta:
        model = Kanban
        fields = ['title', 'is_public']
        labels = {
            'title':'Kanban Title',
            'is_public': 'Visibilty'
        }
        widgets = {
            'title' : forms.TextInput(attrs={'class':"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}),
            'is_public' : forms.RadioSelect(
                choices=VISIBILITY_CHOICES,
                attrs={'class':"flex justify-center gap-5 ms-2 text-sm font-medium text-blue-500 dark:text-gray-300"}
            )
        }