from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Your password must contain at least 8 characters.")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'nick')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nick')
