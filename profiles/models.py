from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.user)

    @property
    def avatar(self):
        try:
            avatar = self.profile_picture.url
        except:
            avatar = static('images/avatar_default.svg')
        return avatar

''' 
When Loggin in:
    Should check if email is a pcu email
        raise error if not
    Should check if is_active is set to True
        Raise error if false
When updating:
    Should change the last updated date
When deactivate:
    Should set is_active to false and then log out
    
'''