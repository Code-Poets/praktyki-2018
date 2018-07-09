from django.test import TestCase
from django.contrib.auth.models import User

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

class NoUserLogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        # not created user

    def test_no_user(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)

class WrongLogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        User.objects.create_user(**self.credentials)

    def test_wrong_login(self):
        response = self.client.post('/login/', 'wronguser', 'nobodypassword', follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)

    def test_wrong_passw(self):
        response = self.client.post('/login/', 'nobodyuser', 'wrongpassword', follow=True)
        # should NOT be logged in now
        self.assertFalse(response.context['user'].is_active)

