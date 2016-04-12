from django.test import TestCase
from django.contrib.auth.models import User
import factory
from imager_profile import models


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('word')
    password = factory.PostGenerationMethodCall('set_password', 'secret')



class SingleUserCreationTestCase(TestCase):

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

    def test_profile_pk_assigned(self):
        self.assertTrue(self.user.pk)

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

    def test_query_from_imager(self):
        query = models.ImagerProfile.objects.get(user__username__exact='warlock')
        self.assertEqual(query, self.profile)


class MultipleUserRelationshipTestCase(TestCase):

    def setUp(self):
        "Create a dictionary of profile objects"
        users = {}
        for username in 'warlock titan hunter'.split():
            users[username] = UserFactory.create(
                username=username,
            )
            users[username].set_password('pulse_rifle')
            users[username].save()
            users[username] = users[username].profile

        self.warlock = users['warlock']
        self.titan = users['titan']
        self.hunter = users['hunter']
        self.warlock.follow('titan')
        self.hunter.follow('warlock')
        self.warlock.save()
        self.hunter.save()
        self.titan.save()

    def test_follow_method(self):
        self.assertTrue(self.titan in self.warlock.following.all())

    def test_reverse_follow_method(self):
        titan_followers = self.titan.followers.all()
        self.assertTrue(self.warlock in titan_followers)

    def test_unfollow_method(self):
        self.warlock.unfollow('titan')
        self.assertFalse(self.titan in self.warlock.following.all())
