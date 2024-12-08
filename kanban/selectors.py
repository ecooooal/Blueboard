from .models import *

def get_kanbans(user):
    kanbans = Kanban.objects.for_user(user)
    return kanbans

def get_specific_kanban_member(user, uuid):
    kanban = Kanban.objects.for_user(user).filter(uuid=uuid)
    return kanban

def participating_kanban(user):
    participating_kanbans = KanbanMember.objects.participating_kanban(user)
    print('adgfasdfas')
    return participating_kanbans

def get_members(kanban):
    member_count = Kanban.objects.get_member(kanban)
    return member_count