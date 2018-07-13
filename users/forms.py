from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'nick')

    email = forms.CharField(label="Email address:", help_text="Required to account verification.")
    nick = forms.CharField(label="Nick name:", help_text="Required. 50 characters or fewer.")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Your password can't be too similar to your other personal information, must contain at least 8 characters, can't be a commonly used password, can't be entirely numeric.")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nick')
