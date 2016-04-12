from django.test import TestCase, Client
from imager_profile.tests.test_model import UserFactory


class IndexPageDefaultViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(
            username='warlock',
        )
        self.user.set_password('pulse_rifle')
        self.user.save()

    def test_index_view_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_404_happens(self):
        response = self.client.get('/invalid/url/nothing/here')
        self.assertEqual(response.status_code, 404)


class StaticFilesTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_static_files_exist(self):
        response = self.client.get('/static/imager_profile/LICENSE.txt')
        self.assertEqual(response.status_code, 200)
