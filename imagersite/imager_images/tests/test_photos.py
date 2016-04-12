from __future__ import unicode_literals
from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from imager_images.models import Photo, Album, privacy_choices
import factory
import random


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('word')
    password = factory.PostGenerationMethodCall('set_password', 'secret')


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Photo

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(privacy_choices)
    # owner = factory.SubFactory(UserFactory, username='BestUser')
    photo = SimpleUploadedFile(name="bg.jpg", content=b"almost an image", content_type='text/png')


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(privacy_choices)
    # owner = factory.SubFactory(UserFactory, username='BestUser')


class SingleImageTestCase(TestCase):

    def setUp(self):
        self.norton = UserFactory.create()
        self.norton.save()
        self.photo = PhotoFactory(
            owner=self.norton.profile
        )

        self.photo.save()

    def test_user_created(self):
        self.assertTrue(self.norton.pk)
