# coding=utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_profile.tests.test_model import UserFactory
from imager_images.models import Photo, Album, PRIVACY_CHOICES
import factory
import random


"""
A quick note about these tests:

A lot of these tests are redundent, I know. The reason they were created was to
help me learn and understand how Factories and Relationship models work. The
best way that I learn was by building tests.

"""

TINY_IMAGE = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x007n\xf9$'
    b'\x00\x00\x00\x10IDATx\x9cb`\x01\x00\x00\x00\xff\xff\x03\x00\x00\x06\x00\x05W\xbf\xab\xd4\x00\x00'
    b'\x00\x00IEND\xaeB`\x82'  # very small valid PNG file
)


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Photo

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(PRIVACY_CHOICES)
    photo = SimpleUploadedFile(name="bg.png", content=TINY_IMAGE, content_type='text/png')


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    published = random.choice(PRIVACY_CHOICES)
    date_published = timezone.now()
    date_modified = timezone.now()
    date_uploaded = timezone.now()


class SingleAlbumTestCase(TestCase):

    def setUp(self):
        self.norton = UserFactory.create()
        self.norton.save()
        self.norton = self.norton.profile
        self.album = AlbumFactory(
            owner=self.norton
        )
        self.album.save()

        self.photo_titles = [u'hello%s' % x for x in range(1)]

        for photo_title in self.photo_titles:
            photo = PhotoFactory(
                owner=self.norton
            )
            photo.title = photo_title
            photo.save()
            self.album.add_photo(photo_title)

    def test_images_created(self):
        self.assertEqual(self.album.photos.count(), 1)

    def test_album_created_correctly_with_no_errors(self):
        self.assertTrue(isinstance(self.album, Album))

    def test_album_has_owner(self):
        self.assertTrue(hasattr(self.album, 'owner'))

    def test_album_owner_set_correctly(self):
        self.assertEqual(self.album.owner, self.norton)

    def test_album_photos_set_correctly(self):
        for title in self.photo_titles:
            self.assertTrue(self.album.photos.get(title__exact=title))

    def test_album_contains_attributes(self):
        self.assertTrue(hasattr(self.album, 'title'))
        self.assertTrue(hasattr(self.album, 'description'))
        self.assertTrue(hasattr(self.album, 'photos'))
        self.assertTrue(hasattr(self.album, 'latest_modified'))
        self.assertTrue(hasattr(self.album, 'latest_uploaded'))
        self.assertTrue(hasattr(self.album, 'latest_published'))
        self.assertTrue(hasattr(self.album, 'add_photo'))
        self.assertTrue(hasattr(self.album, 'cover_photo'))
        self.assertTrue(hasattr(self.album, 'published'))


class SingleImageTestCase(TestCase):

    def setUp(self):
        self.norton = UserFactory.create()
        self.norton.save()
        self.norton = self.norton.profile
        self.photo = PhotoFactory(
            owner=self.norton
        )

        self.photo.save()

    def test_user_created(self):
        self.assertTrue(self.norton.pk)

    def test_photo_meta_created(self):
        self.assertTrue(hasattr(self.photo, 'pk'))
        self.assertTrue(hasattr(self.photo, 'title'))
        self.assertTrue(hasattr(self.photo, 'description'))
        self.assertTrue(hasattr(self.photo, 'date_uploaded'))
        self.assertTrue(hasattr(self.photo, 'date_modified'))
        self.assertTrue(hasattr(self.photo, 'date_published'))
        self.assertTrue(hasattr(self.photo, 'published'))
        self.assertTrue(hasattr(self.photo, 'photo'))

    def test_pk_assigned(self):
        self.assertTrue(self.photo.pk)

    def test_title_is_str(self):
        self.assertEqual(self.photo.title, str(self.photo))

    def test_owner_bind_exists(self):
        self.assertTrue(hasattr(self.photo, 'owner'))

    def test_owner_bind_is_correct(self):
        self.assertEqual(self.photo.owner, self.norton)

    def test_date_metas(self):
        import datetime
        self.assertTrue(isinstance(self.photo.date_uploaded, datetime.datetime))
        self.assertTrue(isinstance(self.photo.date_modified, datetime.datetime))

    def test_published_date_is_false(self):
        import datetime
        self.assertFalse(isinstance(self.photo.date_published, datetime.datetime))

    def test_photo_upload_exists(self):
        self.assertTrue(self.photo.photo)

    def test_photo_upload_correctly(self):
        self.assertTrue(self.photo.photo.read() == TINY_IMAGE)

    def test_photo_attributes_exist(self):
        self.assertTrue(hasattr(self.photo.photo, 'url'))
        self.assertTrue(hasattr(self.photo.photo, 'path'))
