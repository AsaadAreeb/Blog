from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
# Create your models here.

def user_profile_image_path(instance, filename):
    # Get the username of the associated user
    username = instance.user.username
    # The file will be uploaded to 'profile_pics/username/filename'
    return f'profile_pics/{username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=user_profile_image_path)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):

        # checks if the uploaded pic is new or same old pic, 
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image:
                if  this.image.name != 'default.jpg':
                    this.image.delete(save=False)       # delete the old pic

        except:
            pass

        super().save(*args, **kwargs)           # this will save the new uploaded pic

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)