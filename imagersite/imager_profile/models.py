from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ImagerProfile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, related_name="profile")
    camera = models.CharField(max_length=255)
    personality_type = models.CharField(max_length=4)
    category = models.CharField(max_length=255)
    github = models.URLField(blank=True)
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False)

    @property
    def is_active(self):
        return self.user.is_active

    def follow(self, target):
        profile = ImagerProfile.objects.get(user__username__exact=target)
        self.following.add(profile)

    def unfollow(self, target):
        profile = ImagerProfile.objects.get(user__username__exact=target)
        self.following.remove(profile)
