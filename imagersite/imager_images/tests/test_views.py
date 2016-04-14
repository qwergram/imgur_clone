from django.test import TestCase, Client
from django.core import mail
from imager_profile.tests.test_model import UserFactory
from .test_photos import PhotoFactory, AlbumFactory

class LibraryImageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.photo = PhotoFactory.create(
            owner=self.user.profile
        )
        self.private_photo = PhotoFactory.create(
            owner=self.user.profile,
            published="CLOSED"
        )
        self.response = self.client.get('/images/library/')

    def test_view_exists(self):
        self.assertTrue(self.response.status_code == 200)

    def test_view_is_correct(self):
        self.assertTrue("<h1>YOU ARE AT LIBRARY VIEW!</h1>" in self.response.content.decode())

    def view_contains_images(self):
        self.assertTrue('<article class="thumb">' in self.response.content.decode())

    def view_contains_images_except_private(self):
        self.assertFalse(self.private_photo.title in self.response.content.decode())


class AlbumViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = UserFactory.create()
        self.photo = PhotoFactory.create(
            owner=self.user.profile
        )
        self.album = AlbumFactory.create(
            owner=self.user.profile
        )
        self.album.add_photo(self.photo)
        self.album.save()
        self.response = self.client.get('/images/album/{}/'.format(self.album.id))

    def test_view_album_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_album_model_is_correct(self):
        self.assertTrue(self.photo in self.album.photos.all())

    def test_view_album_view_is_correct(self):
        self.assertTrue(self.photo.title in self.response.content.decode())

class PhotoViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/photos/')
