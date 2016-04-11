from django.tests import TestCase
from django.contrib.auth.models import User
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class UserTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username='warlock',
        )
        self.user.set_password('pulse_rifle')


    def test_user_created(self):
        self.assertEquals(self.user.username, 'warlock')
