from django.db import models
from imager_profile.models import ImagerProfile

# Create your models here.

privacy_choices = (
    ('CLOSED', 'Private'),
    ('UNLISTED', 'Shared'),
    ('OPEN', 'Public')
)


class MetaDataMixin:
    "Metadata that is related to both albums and photos."
    owner = models.ForeignKey(ImagerProfile)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published = models.CharField(choices=privacy_choices, max_length=16)
    date_uploaded = models.DateTimeField()
    date_modified = models.DateTimeField()
    date_published = models.DateTimeField()


class Photo(models.Model, MetaDataMixin):
    "A single photo that can be uploaded by a user."

    def __str__(self):
        return self.title

    photo = models.ImageField(upload_to='media')


class Album(models.Model, MetaDataMixin):
    "A collection of photos that be uploaded by a user."
    def __str__(self):
        return self.title
    photos = models.ManyToManyField('Photo', related_name='starred_in')

    @property
    def latest_modified(self):
        "Get the latest modified photo"
        return self.photos.order_by('-date_modified')[0]

    @property
    def latest_published(self):
        "Get the latest published photo"
        return self.photos.order_by('-date_published')[0]

    @property
    def latest_uploaded(self):
        "Get the latest uploaded photo"
        return self.photos.order_by('-date_uploaded')[0]
