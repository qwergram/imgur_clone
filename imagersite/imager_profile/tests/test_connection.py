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
        self.profile = models.ImagerProfile.objects.all()[0]

    def test_user_created(self):
        self.assertEquals(self.user.username, 'warlock')

    def test_profile_created(self):
        self.assertTrue(models.ImagerProfile.objects.all())

    def test_user_to_profile_connection_created(self):
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_profile_to_user_connection_created(self):
        self.assertTrue(hasattr(self.profile, 'user'))

    def test_user_to_profile_connection_is_correct(self):
        self.assertEqual(self.user.profile, self.profile)

    def test_profile_to_user_connection_is_correct(self):
        self.assertEqual(self.profile.user, self.user)

    def test_profile_string(self):
        self.assertEqual(str(self.profile), 'warlock')
