from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password1', 'password2']