from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Your password must contain at least 8 characters.")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'nick')

    def clean(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        if password1 and password2 and (password1 == password2):
            return self.cleaned_data
        else:
            raise forms.ValidationError("Passwords don't match")


class CustomUserChangeForm(UserChangeForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Your password must contain at least 8 characters.")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nick')

    def clean(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        if password1 and password2 and (password1 == password2):
            return self.cleaned_data
        else:
            raise forms.ValidationError("Passwords don't match")
