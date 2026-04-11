from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from apps.mixins import BootstrapMixin


class UserCreateForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']


class UserEditForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
