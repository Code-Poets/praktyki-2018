from django.test import TestCase
from .models import CustomUser
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm


class EditProfileFormTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        response = self.client.post(reverse("signup"), self.credentials, follow=True)

    def test_correct_data(self):
        valid_data = {
            'username': 'new_nobodyuser',
            'email': 'new_nobody@example.com',
            'nick': 'new_nobodys_nick'}
        form = CustomUserChangeForm(valid_data)
        self.assertTrue(form.is_valid())

    def test_too_long_username(self):
        valid_data = {
            'username': 'foqw;efnwldksfalsdkjfosaidfj;alsdfjsadlfkjslakdjfsladkfjslakdjfsdalfkjaslkfaslkdfjaslkdjf',
            'email': 'new_nobody@example.com',
            'nick': 'new_nobodys_nick'}
        form = CustomUserChangeForm(valid_data)
        self.assertFalse(form.is_valid())

    def test_wrong_email(self):
        valid_data = {
            'username': 'new_nobodyuser',
            'email': 'new_nobody',
            'nick': 'new_nobodys_nick'}
        form = CustomUserChangeForm(valid_data)
        self.assertFalse(form.is_valid())

    def test_no_username(self):
        valid_data = {
            'username': '',
            'email': 'new_nobody@example.com',
            'nick': 'new_nobodys_nick'}
        form = CustomUserChangeForm(valid_data)
        self.assertFalse(form.is_valid())

    def test_no_email(self):
        valid_data = {
            'username': 'nobodyuser',
            'email': '',
            'nick': 'new_nobodys_nick'}
        form = CustomUserChangeForm(valid_data)
        self.assertFalse(form.is_valid())

    def test_no_nick(self):
        valid_data = {
            'username': 'nobodyuser',
            'email': 'new_nobody@example.com',
            'nick': ''}
        form = CustomUserChangeForm(valid_data)
        self.assertFalse(form.is_valid())

    def test_edit_profile(self):
        valid_data = {
            'username': 'new_nobodyuser',
            'email': 'new_nobody@example.com',
            'nick': 'new_nobodys_nick'}
        # log in
        self.client.login(username ="nobodyuser", password="passwduser")
        # should be logged in now
        self.assertIn('_auth_user_id', self.client.session)

        # check edit profile content
        response = self.client.get(reverse('edit_profile'))
        self.assertContains(response, 'name="username" value="nobodyuser"')

        # change profile
        response = self.client.post(reverse('edit_profile'), valid_data, follow=True)
        # check edit profile content
        self.assertContains(response, 'name="username" value="new_nobodyuser"')
        self.assertContains(response, 'name="email" value="new_nobody@example.com"')
        self.assertContains(response, 'name="nick" value="new_nobodys_nick"')

        # log out
        self.client.logout()
        # try to log in with old data
        self.client.login(username ="nobodyuser", password="passwduser")
        # should NOT be logged in now
        self.assertNotIn('_auth_user_id', self.client.session)

        # try to log in with new data
        self.client.login(username ="new_nobodyuser", password="passwduser")
        # should be logged in now
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(reverse('games:game_access'), valid_data, follow=True)
        self.assertContains(response, 'name="nick" value="new_nobodys_nick"')

