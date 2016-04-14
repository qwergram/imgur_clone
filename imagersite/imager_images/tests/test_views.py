from django.test import TestCase, Client
from django.core import mail
from imager_profile.tests.test_model import UserFactory
from .test_photos import PhotoFactory, AlbumFactory

class LibraryImageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/library/')

    def test_view_exists(self):
        self.assertTrue(self.response.status_code == 200)

    def test_view_is_correct(self):
        self.assertTrue("<h1>YOU ARE AT LIBRARY VIEW!</h1>" in self.response.content.decode())

class AlbumViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/album/')


class PhotoViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/photos/')
