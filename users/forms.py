from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='логин')
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='павтор пароля', widget=forms.PasswordInput)
    phone = forms.CharField(label='телефон')
    email = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'phone', 'email')
