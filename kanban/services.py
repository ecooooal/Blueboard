from django.core.exceptions import ValidationError
from .models import *


def create_kanban(form, user):
    try:
        kanban = form.save(commit=False)
        kanban.profile = user.profile

        kanban.populate_created_and_updated()
        kanban.full_clean()
        kanban.save()

        add_kanban_member(None, kanban, user)

        return kanban, None

    except ValidationError as e:
        return None, e.messages

def edit_kanban(form, user):
    try:
        kanban = form.save(commit=False)
        kanban.updated_by = user.profile
        kanban.full_clean()
        kanban.save()

        return kanban, None

    except ValidationError as e:
        return None, e.error_dict


def add_kanban_member(request, kanban, user):
    try:
        kanban_member =  KanbanMember(kanban=kanban, profile=user.profile)
        kanban_member.populate_created_and_updated()
        if request is not None:
            kanban_member.updated_by=request.user.profile
        kanban_member.full_clean()
        kanban_member.save()

        return kanban, None

    except ValidationError as e:
        return None, e.messages

