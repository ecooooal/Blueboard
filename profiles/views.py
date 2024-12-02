from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import *
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
def profile_detail_view(request, username=None):
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
    if request.htmx:
        return render(request, 'snippets/profile_detail_snippets.html', context)

@login_required
def profile_detail_edit_view(request):

    if request.method == 'POST':
        form = ProfileNameForm(request.POST, instance = request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileNameForm(instance=request.user.profile)

    return render(request, 'snippets/detail_edit_snippets.html', {'form': form})

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

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    next_page = "/"

    def user_exist(self):
        users = User.objects.all()
        if self.request in users:
            return redirect('home')
        pass

    def user_activate(self):
        profile = self.request.user.profile

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        user1 = request.user
        print(email, password, user, user1)
        if user is None:
            return redirect('profile')

        return super().get(request, *args, **kwargs)
