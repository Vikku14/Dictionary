from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from os import path
from django.db.models.signals import post_save
from django.utils.timezone import now
# Create your models here.

class Profile(models.Model):
    """ Profile for user."""

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


    def get_picture(self):
        no_picture = path.join(settings.MEDIA_URL, 'app/user.png')
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception as e:
            return no_picture

    def __str__(self):
        return self.user.username


def upload_location(instance, filename):
    name, ext = filename.split('.')
    filename = 'profile_picture.'+ str(ext)
    return f"{instance.user.id}/{filename}"

class ProfilePhoto(models.Model):
    ''' Profile picture of user '''

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    photo = models.ImageField(upload_to = upload_location, blank=True, default='app/user.svg')
    uploaded_at = models.DateTimeField(auto_now =True)


    def __str__(self):
        return f"{self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        ProfilePhoto.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profilephoto.save()
