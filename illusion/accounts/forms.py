from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control input-sm',
                                                           'placeholder': 'Username'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'type': "password", 'name': 'password',
                                          'id': "password", 'class': "form-control input-sm",
                                          'placeholder': "Password"}),
    )
    remember_me = forms.BooleanField(help_text='Remember me', required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'type': "password",
            'name': 'password',
            'id': "password",
            'class': "form-control input-sm",
            'placeholder': "Password"
        }
        )
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'type': "password",
            'name': 'password',
            'id': "password",
            'class': "form-control input-sm",
            'placeholder': "Confirm password"
        }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': "form-control input-sm", 'placeholder': 'Email'})
        }