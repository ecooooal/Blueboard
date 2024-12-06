from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .selectors import *

def home_view(request):
    kanbans = get_kanbans(request.user)
    context = {
        'kanbans':kanbans
    }
    return render(request, 'homepage.html', context)

def create_kanban_view(request):
    form = KanbanCreateForm()
    print('hello')
    if request.method == 'POST':
        form = KanbanCreateForm(request.POST)
        if form.is_valid():
            kanban = form.save(commit=False)
            kanban.profile = request.user.profile
            kanban.save()
            return redirect('home')
    else:
        print('raw form')
        return render(request, 'kanban/create_kanban.html', {'form':form})