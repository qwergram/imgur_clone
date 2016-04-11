from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ImagerProfile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User)
    camera = models.CharField(max_length=255)
    personality_type = models.CharField(max_length=4)
    category = models.CharField(max_length=255)
    github = models.URLField(blank=True)
