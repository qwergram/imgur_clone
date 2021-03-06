# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from imager_profile.models import ImagerProfile

# Create your models here.


PRIVATE = 'CLOSED'
UNLISTED = 'UNLISTED'
PUBLIC = 'OPEN'
PRIVACY_CHOICES = (
    (PRIVATE, 'Private'),
    (UNLISTED, 'Shared'),
    (PUBLIC, 'Public')
)


def image_path(instance, file_name):
    return 'media/{0}/{1}'.format(instance.owner.id, file_name)


class Photo(models.Model):
    """A single photo that can be uploaded by a user."""

    def __str__(self):
        return self.title

    owner = models.ForeignKey(ImagerProfile)
    title = models.CharField(max_length=255, default="Example Title")
    description = models.TextField(default="Write a short description about your photo!", max_length=1024)
    published = models.CharField(choices=PRIVACY_CHOICES, max_length=255, default=PUBLIC)

    date_uploaded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_published = models.DateTimeField(null=True, blank=True)

    photo = models.ImageField(upload_to=image_path)


class Album(models.Model):
    """A collection of photos that be uploaded by a user."""
    def __str__(self):
        return self.title

    owner = models.ForeignKey(ImagerProfile)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published = models.CharField(choices=PRIVACY_CHOICES, max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    date_published = models.DateTimeField(null=True, blank=True)

    photos = models.ManyToManyField('Photo', related_name='starred_in')
    cover_photo = models.ForeignKey(Photo, blank=True, null=True)

    @property
    def latest_modified(self):
        """Get the latest modified photo"""
        return self.photos.order_by('-date_modified')[0]

    @property
    def latest_published(self):
        """Get the latest published photo"""
        return self.photos.order_by('-date_published')[0]

    @property
    def latest_uploaded(self):
        """Get the latest uploaded photo"""
        return self.photos.order_by('-date_uploaded')[0]

    def add_photo(self, photo):
        photo = str(photo)
        if photo and isinstance(photo, str):
            photo_result = Photo.objects.get(title=photo)
            if photo_result:
                photo = photo_result
        if not isinstance(photo, Photo):
            raise TypeError("%s is not a Photo or str object (%s)" % (Photo, type(photo)))

        self.photos.add(photo)
