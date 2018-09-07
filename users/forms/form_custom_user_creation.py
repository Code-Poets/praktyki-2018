from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, help_text=_("Your password must contain at least 8 characters."))
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput, help_text=_("Enter the same password as above, for verification."))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'nick')
