# coding=utf-8
from django.test import TestCase, Client
from django.shortcuts import resolve_url
from imager_profile.tests.test_model import UserFactory
from .test_photos import PhotoFactory, AlbumFactory
from imager_images.models import PRIVATE, PUBLIC


class LibraryImageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.photo = PhotoFactory.create(
            owner=self.user.profile
        )
        self.private_photo = PhotoFactory.create(
            owner=self.user.profile,
            published=PRIVATE
        )
        self.response = self.client.get(resolve_url('library'))

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

        self.user = UserFactory.create(
            username="user",
            password="password",
        )
        self.photo = PhotoFactory.create(
            owner=self.user.profile
        )
        self.album = AlbumFactory.create(
            owner=self.user.profile
        )
        self.album.add_photo(self.photo)
        self.response = self.client.get(resolve_url('albums', album_id=self.album.id))

    def test_view_album_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_album_model_is_correct(self):
        self.assertTrue(self.photo in self.album.photos.all())

    def test_view_album_view_is_correct(self):
        self.assertContains(self.response, self.photo.title)

    def test_album_shows_in_library(self):
        _ = self.client.get(resolve_url('auth_login'), {
            'username': self.user.username,
            'password': "password",
        })
        library_response = self.client.get(resolve_url('library'))
        self.assertContains(library_response, resolve_url('albums', album_id=self.album.id))


class PrivatePhotoViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.photo = PhotoFactory.create(
            owner=self.user.profile,
            published=PRIVATE,
        )

    def test_photo_page_404s(self):
        detail_response = self.client.get(resolve_url('photos_view', photo_id=self.photo.id))
        self.assertEqual(detail_response.status_code, 404)

    # def test_photo_url_404s(self):
    #     photo_response = self.client.get(self.photo.photo.url)
    #     self.assertEqual(photo_response.status_code, 404)

    def test_private_photo_does_not_shuffle_into_main_page(self):
        front_page_response = self.client.get(resolve_url('homepage'))
        self.assertNotContains(front_page_response, self.photo.photo.url)


class OwnPrivatePhotoViewTestcase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(
            username="skdfjlaksjd",
            password="password",
        )
        self.user.save()
        self.photo = PhotoFactory.create(
            owner=self.user.profile,
            published=PRIVATE,
        )
        self.photo.save()
        self.client.post(resolve_url('auth_login'), {
            'username': self.user.username,
            'password': "password"
        })

    def test_own_private_photo_appears(self):
        detail_response = self.client.get(resolve_url('photos_view', photo_id=self.photo.id))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.photo.photo.url)

    # def test_own_private_photo_file_exists(self):
    #     photo_response = self.client.get(self.photo.photo.url)
    #     self.assertEqual(photo_response.status_code, 200)


class PublicPhotoViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(
            username="bob"
        )
        self.user.set_password("password")
        self.user.save()
        self.photo = PhotoFactory.create(
            owner=self.user.profile,
            published=PUBLIC,
        )
        self.photo.save()
        self.client.post(resolve_url('auth_login'), {
            'username': self.user.username,
            'password': "password"
        })

    def test_photo_page_exists(self):
        detail_response = self.client.get(resolve_url('photos_view', photo_id=self.photo.id))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.photo.photo.url)

    # def test_photo_exists(self):
    #     photo_response = self.client.get(self.photo.photo.url)
    #     self.assertEqual(photo_response.status_code, 200)

    def test_public_photo_shuffles_into_main_page(self):
        front_page_response = self.client.get(resolve_url('homepage'))
        self.assertContains(front_page_response, self.photo.photo.url)
