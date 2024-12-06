from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .selectors import *

def home_view(request):
    if request.user.is_authenticated:
        my_kanbans = get_kanbans(request.user)
        participating_kanbans = participating_kanban(request.user)

        context = {
            'kanbans': my_kanbans,
            'participating': participating_kanbans
        }

        return render(request, 'homepage.html', context)
    else:
        return render(request, 'homepage.html')

def create_kanban_view(request):
    form = KanbanCreateForm()

    if request.method == 'POST':
        form = KanbanCreateForm(request.POST)
        if form.is_valid():
            kanban = form.save(commit=False)
            kanban.profile = request.user.profile
            kanban.save()
            return redirect('home')
    else:
        return render(request, 'kanban/create_kanban.html', {'form':form})