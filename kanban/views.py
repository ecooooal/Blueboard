from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_htmx.http import retarget
from django.contrib import messages
from .forms import *
from .selectors import *
from .services import *
from .models import *

def home_view(request):
    if request.user.is_authenticated:
        my_kanbans = get_kanbans(request.user)
        participating_kanbans = KanbanMember.objects.participating_kanban(request.user)
        print("My Kanbans: ", my_kanbans)  # Check the content of 'my_kanbans'
        print("Participating Kanbans: ", participating_kanbans)  # Check the content of 'participating_kanbans'

        context = {
            'kanbans': my_kanbans,
            'participating': participating_kanbans
        }

        return render(request, 'homepage.html', context)
    else:
        return render(request, 'homepage.html')

def kanban_page_view(request, uuid:Kanban.uuid):
    kanban = get_object_or_404(Kanban, uuid=uuid)
    context = {
        'kanban':kanban
    }
    return render(request, 'kanban/kanban_page.html', context)

def kanban_page_detail_view(request, uuid:Kanban.uuid):
    kanban = get_object_or_404(Kanban.objects.annotate(member_count=Count('members')), uuid=uuid)
    context = {
        'kanban':kanban
    }
    if request.htmx:
        return render(request, 'kanban/kanban_page_details.html', context)

def add_kanban_member_view(request, uuid):
    kanban = get_object_or_404(Kanban, uuid=uuid)
    context = {
        'kanban':kanban
    }
    if request.method == 'POST':
        put_kanban = Kanban.objects.get(uuid=uuid)
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'User with username "{username}" does not exist.')
            return redirect('kanban_page', uuid=uuid)

        if KanbanMember.objects.filter(kanban=put_kanban, profile=user.profile).exists():
            messages.error(request, f'{username} is already a member of this Kanban.')
            return redirect('kanban_page', uuid=uuid)

        add_kanban_member(request, put_kanban, user)
        messages.success(request, f'{username} has been added as a member of the Kanban.')


    return render(request, 'kanban/kanban_page.html', context)

@login_required
def create_kanban_view(request):
    form = KanbanCreateForm()

    if request.method == 'POST':
        form = KanbanCreateForm(request.POST)
        if form.is_valid():
            kanban, errors = create_kanban(form, request.user)

            if kanban:
                return redirect('home_redirect')
            else:
                for error in errors:
                    form.add_error(None, error)
                response = render(request, 'kanban/create_kanban.html', {'form': form})
                return retarget(response, '#kanbanModal')

    else:
        return render(request, 'kanban/create_kanban.html', {'form':form})

def kanban_edit_view(request, uuid):
    kanban = get_object_or_404(Kanban, uuid=uuid)
    form = KanbanCreateForm(instance=kanban)
    context = {
        'kanban': kanban,
        'form': form,
    }
    if request.method == 'POST':
        form = KanbanCreateForm(request.POST, instance=kanban)
        if form.is_valid():
            pass_kanban, errors = edit_kanban(form, request.user)

            if pass_kanban:
                return render(request, 'kanban/kanban_page.html', {'kanban':pass_kanban})
            else:
                for field, errors in errors.items():
                    for error in errors:
                        form.add_error(field, error)
                response = render(request, 'kanban/kanban_edit.html', {'kanban': kanban,'form': form})
                return retarget(response, '#thisBody')
    else:
        return render(request, 'kanban/kanban_edit.html', context)

@login_required
def kanban_delete_view(request, uuid):
    kanban = get_object_or_404(Kanban, uuid=uuid)
    context = {
        'kanban': kanban
    }
    if request.method == "POST":
        kanban.is_active = False
        kanban.save()
        return redirect('home')
    else:
        return render(request, 'kanban/kanban_delete.html', context)
    return redirect('home')

def kanban_board_view(request, uuid):
    kanban = get_object_or_404(Kanban, uuid=uuid)
    kanban2 = Kanban.objects.prefetch_related('columns').prefetch_related('columns__cards').get(uuid=uuid)
    columns = kanban2.columns.all()
    context = {
        'kanban':kanban,
        'columns':columns
    }
    return render(request, 'kanban/kanban_board.html', context)

def card_detail_view(request, card_id, uuid):
    kanban = get_object_or_404(Kanban, uuid=uuid)
    print(kanban)
    card = get_object_or_404(Card, id=card_id)
    print(card)
    context = {
        'kanban': kanban,
        'card': card,
    }
    print(type(card.id))
    response = render(request, 'kanban/card_detail.html', context)
    return retarget(response, '#boardContent')