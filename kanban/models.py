from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, related_name='+')
    updated_by = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, related_name='+')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Kanban(BaseModel):
    profile = models.ForeignKey('profiles.Profile', on_delete=models.PROTECT, related_name='kanbans', null=False)
    title = models.CharField(max_length=250)
    is_public = models.BooleanField(default=False)

class Column(BaseModel):
    kanban = models.ForeignKey('Kanban', on_delete=models.PROTECT, related_name='columns', null=False)
    title = models.CharField(max_length=250)
    position = models.PositiveIntegerField()
    card_limit = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']  # Ensures columns are ordered by position in queries

class Card(BaseModel):
    column = models.ForeignKey('Column', on_delete=models.PROTECT, related_name='cards', null=False)
    title = models.CharField(max_length=250)
    description = models.TextField()
    position = models.PositiveIntegerField()
    card_limit = models.PositiveIntegerField()
    due_date = models.DateTimeField()

class CardAttachment(BaseModel):
    card = models.ForeignKey('Card', on_delete=models.PROTECT, related_name='card_attachments', null=False)
    filename = models.CharField(max_length=250)
    attachment = models.FileField(upload_to='uploads/attachments/%Y/%m/%d/', null=True, blank=True)

class CardThumbnail(BaseModel):
    card = models.ForeignKey('Card', on_delete=models.PROTECT, related_name='card_thumbnails', null=False)
    filename = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/%Y/%m/%d/', null=True, blank=True)

class KanbanMember(BaseModel):
    kanban = models.ForeignKey(Kanban, related_name="members", on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', related_name="kanban_members", on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('kanban', 'profile')
