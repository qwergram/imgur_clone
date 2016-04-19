# coding=utf-8
from django.test import TestCase, Client
from django.shortcuts import resolve_url
from django.core import mail
from imager_profile.tests.test_model import UserFactory
from django.contrib.staticfiles import finders
import os
import io


class LoginPageViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(resolve_url('auth_login'))

    def test_login_view_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_view_contains_a_form(self):
        self.assertContains(self.response, '<form')

    def test_login_contains_submit(self):
        self.assertContains(self.response, '<input type="submit"')


class AuthenticateViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.client = Client()
        self.response = self.client.post(resolve_url('auth_login'), {
            "username": self.user.username,
            "password": "icantsayit"
        })

    def test_login_page_redirects(self):
        self.assertEqual(self.response.status_code, 302)

    def test_login_page_redirect_location(self):
        self.assertEqual(self.response.url, resolve_url('profile'))

    def test_login_page_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(resolve_url('auth_login'), {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.assertEqual(response.status_code, 403)


class OwnProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.client = Client()
        login_response = self.client.post(resolve_url('auth_login'), {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.response = self.client.get(login_response.url)

    def test_profile_page_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_logout_button_appears(self):
        self.assertContains(self.response, ' class="button">Log Out</a></li>')

    def test_login_doesnt_exist(self):
        self.assertNotContains(self.response, ' class="button">Log In</a></li>')

    def test_register_doesnt_exist(self):
        self.assertNotContains(self.response, ' class="button">Register</a></li>')

    def test_username_appears(self):
        self.assertContains(self.response, self.user.username)

    def test_static_image_appears(self):
        self.assertContains(self.response, '<!-- no public photos -->')


class LogoutPageViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.client = Client()
        self.client.post(resolve_url('auth_login'), {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.response = self.client.get(resolve_url('auth_logout'))

    def test_check_logout_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_checkout_logout_hacked_302(self):
        self.assertContains(self.response, '<meta http-equiv="refresh" content="0;URL=/">')


class RegisterPageViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(resolve_url('registration_register'))

    def register(self):
        return self.client.post(resolve_url('registration_register'), {
            "username": "kent",
            "email": "kent@hiscompany.com",
            "password1": "wablwabl3",
            "password2": "wablwabl3"
        })

    def test_register_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_register_contains_forms(self):
        self.assertContains(self.response, '<form ')

    def test_register_success(self):
        response = self.client.post(resolve_url('registration_register'), {
            "username": "kent",
            "email": "kent@hiscompany.com",
            "password1": "wabl",
            "password2": "wabl"
        })
        self.assertEqual(response.status_code, 200)

    def test_register_form_submit_works(self):
        response = self.register()
        self.assertEqual(response.status_code, 302)

    def test_register_email_created(self):
        _ = self.register()
        self.assertEqual(len(mail.outbox), 1)

    def test_register_email_address_correct(self):
        _ = self.register()
        letter = mail.outbox[0]
        self.assertEqual(letter.recipients()[0], "kent@hiscompany.com")

    def test_register_email_content_correct(self):
        _ = self.register()
        letter = mail.outbox[0]
        self.assertTrue("Click here to complete your Registration\n</a>" in letter.message().get_payload())
        self.assertTrue("- Waffles" in letter.message().get_payload())

    def test_register_short_password(self):
        response = self.client.post(resolve_url('registration_register'), {
            "username": "kent",
            "email": "kent@hiscompany.com",
            "password1": "wabl",
            "password2": "wabl"
        })
        self.assertContains(response, '<form ')

    def test_register_email_link_works(self):
        self.register()
        letter = mail.outbox[0]
        email_link = letter.message().get_payload().split('\n')[0].split('"')[1]
        email_link_response = self.client.get(email_link)
        self.assertEqual(email_link_response.status_code, 302)
        self.assertTrue(email_link.startswith(resolve_url('registration_activate', activation_key="a")[:-2]))
        self.assertEqual(email_link_response.url, resolve_url('registration_activation_complete'))

    def test_accounts_complete_view(self):
        response = self.client.get(resolve_url('registration_activation_complete'))
        self.assertEqual(response.status_code, 200)

    def test_accounts_complete_view_content_correct(self):
        response = self.client.get(resolve_url('registration_activation_complete'))
        self.assertContains(response, "<h1> Thanks for signing up! </h1>")


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
        self.assertContains(self.response, '/static/imager_profile/assets/css/main.css')

    def test_index_handles_lt_ie8(self):
        self.assertContains(self.response, '/static/imager_profile/assets/js/ie/html5shiv.js')
        self.assertContains(self.response, '/static/imager_profile/assets/js/ie/respond.min.js')
        self.assertContains(self.response, '/static/imager_profile/assets/css/ie8.css')
        self.assertContains(self.response, '/static/imager_profile/assets/css/ie9.css')

    def test_javascript_libraries_load(self):
        self.assertContains(self.response, '/static/imager_profile/assets/js/jquery.min.js')
        self.assertContains(self.response, '/static/imager_profile/assets/js/skel.min.js')
        self.assertContains(self.response, '/static/imager_profile/assets/js/util.js')
        self.assertContains(self.response, '/static/imager_profile/assets/js/main.js')

    def test_index_view_is_not_base_view(self):
        self.assertNotContains(self.response, '<p>Hello World!</p>')

    def test_login_button_appears(self):
        self.assertContains(self.response, 'class="button">Log In</a>')

    def test_register_button_appears(self):
        self.assertContains(self.response, ' class="button">Register</a></li>')

    def test_username_filler_appears(self):
        self.assertContains(self.response, 'Imgur Clone')


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


class OtherProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            username="kent"
        )
        self.user.set_password("icantsayit")
        self.user.save()
        self.user2 = UserFactory.create(
            username="norton"
        )
        self.user2.set_password("icantsayit")
        self.user2.save()
        self.client = Client()
        self.client.post(resolve_url('auth_login'), {
            "username": self.user.username,
            "password": "icantsayit"
        })
        self.response = self.client.get('/profile/')
        self.response2 = self.client.get('/profile/{}/'.format(self.user2.profile.id))

    def test_proflie_url_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_other_profile_exists(self):
        self.assertEqual(self.response2.status_code, 200)

    def test_profile_url_is_correct(self):
        self.assertContains(self.response, "<h1>YOU ARE AT PROFILES</h1>")

    def test_profile_name_appears(self):
        self.assertContains(self.response, 'kent</a></h1>')

    def test_other_profile_appears(self):
        self.assertContains(self.response2, 'norton</a></h1>')
