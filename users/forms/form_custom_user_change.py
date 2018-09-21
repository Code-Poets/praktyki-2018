from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nick')

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')

    def clean_password(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        return self.cleaned_data
