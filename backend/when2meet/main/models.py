from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    pic = models.ImageField(upload_to="profile_pics", default="default_profile_pic.jpg")
    class Meta:
        ordering = ["-date_joined"]

class Event(models.Model):
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    anonowner = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=250)
    # description = models.CharField(max_length=500)
    time = models.CharField(max_length=250)
    possible_time = models.CharField(max_length=250)

class Available(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    anonuser = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=250)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time = models.CharField(max_length=250)