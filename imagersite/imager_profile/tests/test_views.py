from django.test import TestCase, Client
from imager_profile.tests.test_model import UserFactory
from django.contrib.staticfiles import finders
import os
import io


class LoginPageViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/accounts/login/')

    def test_login_view_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_view_contains_a_form(self):
        self.assertTrue('<form' in self.response.content.decode())

    def test_login_contains_submit(self):
        self.assertTrue('<input type="submit"' in self.response.content.decode())


class AuthenticateViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.client = Client()
        self.response = self.client.post('/accounts/login/', {
            "username": self.user.username,
            "password": "icantsayit"
        })

    def test_login_page_redirects(self):
        self.assertEqual(self.response.status_code, 302)

    def test_login_page_redirect_location(self):
        self.assertEqual(self.response.url, '/')

    def test_login_page_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post('/accounts/login/', {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.assertEqual(response.status_code, 403)


class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.client = Client()
        self.client.post('/accounts/login/', {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.response = self.client.get('/')

    def test_profile_page_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_logout_button_appears(self):
        self.assertTrue(' class="button big fit">Log Out</a></li>' in self.response.content.decode())

    def test_login_doesnt_exist(self):
        self.assertFalse(' class="button big fit">Log In</a></li>' in self.response.content.decode())

    def test_register_doesnt_exist(self):
        self.assertFalse(' class="button big fit">Register</a></li>' in self.response.content.decode())


class LogoutPageViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.client = Client()
        self.client.post('/accounts/login/', {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.response = self.client.get('/accounts/logout/')

    def test_check_logout_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_checkout_logout_hacked_302(self):
        self.assertTrue('<meta http-equiv="refresh" content="0;URL=/">' in self.response.content.decode())

class RegisterPageViewTestCase(TestCase):
    pass


class IndexPageDefaultViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/')
        self.user = UserFactory.create(
            username='warlock',
        )
        self.user.set_password('pulse_rifle')
        self.user.save()

    def test_index_view_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_404_happens(self):
        response = self.client.get('/invalid/url/nothing/here')
        self.assertEqual(response.status_code, 404)

    def test_index_contains_proper_static_links(self):
        self.assertTrue('/static/imager_profile/assets/css/main.css' in self.response.content.decode())

    def test_index_handles_lt_ie8(self):
        self.assertTrue('/static/imager_profile/assets/js/ie/html5shiv.js' in self.response.content.decode())
        self.assertTrue('/static/imager_profile/assets/js/ie/respond.min.js' in self.response.content.decode())
        self.assertTrue('/static/imager_profile/assets/css/ie8.css' in self.response.content.decode())
        self.assertTrue('/static/imager_profile/assets/css/ie9.css' in self.response.content.decode())

    def test_javascript_libraries_load(self):
        self.assertTrue('/static/imager_profile/assets/js/jquery.min.js' in self.response.content.decode())
        self.assertTrue('/static/imager_profile/assets/js/skel.min.js' in self.response.content.decode())
        self.assertTrue('/static/imager_profile/assets/js/util.js' in self.response.content.decode())
        self.assertTrue('/static/imager_profile/assets/js/main.js' in self.response.content.decode())

    def test_index_view_is_not_base_view(self):
        self.assertFalse('<p>Hello World!</p>' in self.response.content.decode())

    def test_login_button_appears(self):
        self.assertTrue('class="button big fit">Log In</a>' in self.response.content.decode())

    def test_register_button_appears(self):
        self.assertTrue(' class="button big fit">Register</a></li>' in self.response.content.decode())


class StaticFilesTestCase(TestCase):

    def setUp(self):
        self.client = finders

    def check_exists(self, path):
        self.assertTrue(os.path.exists(path))

    def check_file_is_correct(self, path, startswith):
        self.assertTrue(io.open(path).read().startswith(startswith))

    def test_static_files_exist(self):
        path = self.client.find('imager_profile/LICENSE.txt')
        self.check_exists(path)

    def test_static_files_correct(self):
        path = self.client.find('imager_profile/LICENSE.txt')
        self.check_file_is_correct(path, 'Creative Commons Attribution 3.0 Unported')
