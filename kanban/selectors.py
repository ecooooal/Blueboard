from .models import *

def get_kanbans(user):
    kanbans = Kanban.objects.for_user(user)
    return kanbans

def participating_kanban(user):
    participating_kanbans = KanbanMember.objects.participating_kanban(user)
    return participating_kanbans