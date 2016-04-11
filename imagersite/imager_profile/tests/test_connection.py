from django.test import TestCase
from django.contrib.auth.models import User
import factory
from imager_profile import models

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class UserTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username='warlock',
        )
        self.user.set_password('pulse_rifle')
        self.user.save()

    def test_user_created(self):
        self.assertEquals(self.user.username, 'warlock')

    def test_imgur_object_created(self):
        self.assertTrue(models.ImagerProfile.objects.all())

    def test_imgur_attachement_created(self):
        self.assertTrue(hasattr(self.user, 'profile'))
