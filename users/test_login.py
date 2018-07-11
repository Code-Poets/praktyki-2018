from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        CustomUser.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post(reverse("login"), self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)


class NoUserLogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        # not created user

    def test_no_user(self):
        response = self.client.post(reverse("login"), self.credentials, follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)


class WrongLogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        CustomUser.objects.create_user(**self.credentials)

    def test_wrong_login(self):
        response = self.client.post(reverse("login"), 'wronguser', 'nobodypassword', follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)

    def test_wrong_passw(self):
        response = self.client.post(reverse("login"), 'nobodyuser', 'wrongpassword', follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)

    def test_no_login(self):
        response = self.client.post(reverse("login"), '', 'nobodypassword', follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)

    def test_no_passw(self):
        response = self.client.post(reverse("login"), 'nobodyuser', '', follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)
