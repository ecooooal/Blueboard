from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import *


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    context = {
        'profile':profile,
    }

    return render(request, 'profiles/profile.html', context)
@login_required
def profile_detail_view(request):
    if request.htmx:
        return render(request, 'snippets/profile_detail_snippets.html')
@login_required
def profile_kanban_view(request):
    if request.htmx:
        return render(request, 'snippets/profile_kanban_snippets.html')
@login_required
def profile_account_view(request):
    if request.htmx:
        return render(request, 'snippets/profile_account_snippets.html')
@login_required
def profile_report_view(request):
    if request.htmx:
        return render(request, 'snippets/profile_report_snippets.html')