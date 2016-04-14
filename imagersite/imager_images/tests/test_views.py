from django.test import TestCase, Client
from django.core import mail
from imager_profile.tests.test_model import UserFactory
from .test_photos import PhotoFactory, AlbumFactory

class LibraryImageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/library/')


class AlbumViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/album/')


class PhotoViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/images/photos/')
