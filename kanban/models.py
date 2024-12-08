from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, UniqueConstraint
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, related_name='+')
    updated_by = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, related_name='+')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def populate_created_and_updated(self):
        is_new = self.pk is None
        if is_new:
            if not self.pk and not self.created_by:
                self.created_by = self.profile
        if self.updated_by is None:
            self.updated_by = self.profile
        return None

class KanbanManager(models.Manager):
    def for_user(self, user:User):
        return self.filter(profile=user.profile).annotate(member_count=Count('members'))
    def get_members(self, uuid):
        return self.filter(uuid=uuid).annotate(member_count=Count('members'))

class KanbanMemberManager(models.Manager):
    def participating_kanban(self, user:User):
        return (self.filter(profile=user.profile)
                .annotate(member_count=Count('kanban__members'))
                .exclude(created_by=user.profile))

class Kanban(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.PROTECT, related_name='kanbans', null=False)
    title = models.CharField(max_length=250)
    is_public = models.BooleanField(default=False)
    objects = KanbanManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title','profile'),
                name='kanban_title_unique_to_user',
            )
        ]

    def __str__(self):
        return f'{self.title} : {self.profile.user.first_name} {self.profile.user.last_name}'

class KanbanMember(BaseModel):
    kanban = models.ForeignKey(Kanban, related_name="members", on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', related_name="kanban_members", on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    objects = KanbanMemberManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('kanban','profile'),
                name='kanban_unique_to_user',
            )
        ]

    def __str__(self):
        return f'{self.profile.user.username} : {self.kanban.title} : can edit? {self.can_edit}'




class Column(BaseModel):
    kanban = models.ForeignKey('Kanban', on_delete=models.PROTECT, related_name='columns', null=False)
    title = models.CharField(max_length=250)
    position = models.PositiveIntegerField()
    card_limit = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']  # Ensures columns are ordered by position in queries

    def __str__(self):
        return f'{self.kanban.title} : {self.title}'

class Card(BaseModel):
    column = models.ForeignKey('Column', on_delete=models.PROTECT, related_name='cards', null=False)
    title = models.CharField(max_length=250)
    description = models.TextField()
    position = models.PositiveIntegerField()
    due_date = models.DateTimeField()

    def __str__(self):
        return f'{self.column.kanban.title} : {self.title}'

class CardAttachment(BaseModel):
    card = models.ForeignKey('Card', on_delete=models.PROTECT, related_name='card_attachments', null=False)
    filename = models.CharField(max_length=250)
    attachment = models.FileField(upload_to='uploads/attachments/%Y/%m/%d/', null=True, blank=True)

class CardThumbnail(BaseModel):
    card = models.ForeignKey('Card', on_delete=models.PROTECT, related_name='card_thumbnails', null=False)
    filename = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/%Y/%m/%d/', null=True, blank=True)



