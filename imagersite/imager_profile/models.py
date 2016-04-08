from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ImagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_active(self):
        return self.active
