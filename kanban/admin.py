from django.contrib import admin
from .models import *
# Register your models here.



admin.site.register(Kanban)
admin.site.register(Column)
admin.site.register(Card)
admin.site.register(CardAttachment)
admin.site.register(CardThumbnail)
admin.site.register(KanbanMember)

