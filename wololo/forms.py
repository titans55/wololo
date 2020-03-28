from .models import Users
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate


class RegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )  # ignored
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ["username", "email", "password1", "password2"]

    def clean(self, *args, **kwargs):
        """
        Normal cleanup + username generation.
        """

        cleaned_data = super(UserCreationForm, self).clean(*args, **kwargs)
        if 'email' in cleaned_data:
            cleaned_data['username'] = cleaned_data['email']

        return cleaned_data
