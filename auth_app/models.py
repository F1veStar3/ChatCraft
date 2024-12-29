from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=2000)
    uuid = models.UUIDField(primary_key=True, editable=False)


