from django.test import TestCase
from django.contrib.auth.models import User
import factory
from imager_images import models
from imager_profile.models import ImagerProfile
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import mock

class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Photo


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class SinglePhotoUploadTestCase(TestCase):

    def setUp(self):
        self.norton = UserFactory.create(
            username='nortonpengra'
        )
        self.norton.save()
        self.photo = PhotoFactory.create()
        self.photo.owner = self.norton.profile
        self.photo.title = 'Some photo',
        self.photo.description = 'Hello World! My name is Norton Pengra!',
        self.photo.published = 'CLOSED',
        # self.photo.photo = SimpleUploadedFile(
        #     name="bg.png",
        #     # file='imagersite/static/bg.jpg',
        #     content=io.open('imagersite/static/bg.jpg', 'rb').read(),
        #     content_type="image/jpg"
        # )[0],

        self.photo.save()

    def test_photo_upload_successful(self):
        self.assertTrue(self.photo.id)

    def test_meta_mixin_works(self):
        photo = PhotoFactory.create()
        self.assertTrue(hasattr(photo, 'owner'))
        self.assertTrue(hasattr(photo, 'title'))
        self.assertTrue(hasattr(photo, 'description'))
        self.assertTrue(hasattr(photo, 'published'))
        self.assertTrue(hasattr(photo, 'photo'))
