from django.test import TestCase
from .models import CustomUser
from .forms import CustomUserCreationForm


class SignUpFormTest(TestCase):
    def test_correct_signup(self):
        valid_data = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(valid_data)
        self.assertTrue(form.is_valid())

    def test_existing_login(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'passwduser'}
        CustomUser.objects.create_user(**self.credentials)
        invalid_data = {
            'username': 'nobodyuser',
            'email': 'else@example.com',
            'nick': 'else_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_no_login(self):
        invalid_data = {
            'username': '',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_no_nick(self):
        invalid_data = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': '',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_no_email(self):
        invalid_data = {
            'username': 'nobodyuser',
            'email': '',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_no_pass1(self):
        invalid_data = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': '',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_no_pass2(self):
        invalid_data = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': ''}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_mismath_passwd(self):
        invalid_data = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduserr'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_too_long_login(self):
        # Username more than 30 character
        invalid_data = {
            'username': 'foqw;efnwldksfalsdkjfosaidfj;alsdfjsadlfkjslakdjfsladkfjslakdjfsdalfkjaslkfaslkdfjaslkdjf',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_too_long_nick(self):
        # Username more than 50 character
        invalid_data = {
            'username': 'foqw;efnwldksfalsdkjdfjaslkdjfdfjaslkdjfdfjaslkdjffosaidfj;alsdfjsadlfkjslakdjfsladkfjslakdjfsdalfkjaslkfaslkdfjaslkdjf',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'passwduser',
            'password2': 'passwduser'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_too_short_passwd(self):
        invalid_data = {
            'username': 'nobodyuser',
            'email': 'nobody@example.com',
            'nick': 'nobodys_nick',
            'password1': 'pass',
            'password2': 'pass'}
        form = CustomUserCreationForm(invalid_data)
        self.assertFalse(form.is_valid())
