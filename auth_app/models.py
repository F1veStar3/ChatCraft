from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from chat_app.models import Chat


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    logo = models.ImageField(upload_to='chatcraft/logo/', blank=True, null=True)
    chats = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, blank=True) # TODO change to many-to-many

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
