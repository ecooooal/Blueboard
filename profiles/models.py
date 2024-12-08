from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.utils import timezone
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default="My Bio...")
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures/%Y/%m/%d/',default='defaults/profile_picture_default.png', null=True, blank=True)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile = Profile.objects.get(user=self.user)
        print(profile.profile_picture.url)

        img = Image.open(self.profile_picture.path)


        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

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