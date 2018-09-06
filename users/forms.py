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

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')

    def clean_password(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        return self.cleaned_data


