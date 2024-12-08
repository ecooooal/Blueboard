from .models import *

def get_kanbans(user):
    return Kanban.objects.for_user(user)

def get_specific_kanban_member(user, uuid):
    kanban = Kanban.objects.for_user(user).filter(uuid=uuid)
    return kanban

def participating_kanban(user):
    return KanbanMember.objects.participating_kanban(user)


def get_members(kanban):
    member_count = Kanban.objects.get_member(kanban)
    return member_count