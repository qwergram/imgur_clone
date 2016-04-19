from django.conf import settings
from django.db import models

# Create your models here.


class ImagerProfile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", max_length=255)
    camera = models.CharField(max_length=255, blank=True)
    personality_type = models.CharField(max_length=4, blank=True)
    category = models.CharField(max_length=255, blank=True)
    github = models.URLField(blank=True, max_length=255)
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False, blank=True, max_length=255)

    @property
    def is_active(self):
        return self.user.is_active

    def follow(self, target):
        profile = ImagerProfile.objects.get(user__username__exact=target)
        self.following.add(profile)

    def unfollow(self, target):
        profile = ImagerProfile.objects.get(user__username__exact=target)
        self.following.remove(profile)
