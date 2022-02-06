from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Bets


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'sector', 'password1', 'password2']


class AddBetForm(ModelForm):
    class Meta:
        model = Bets
        fields = ['bet_name', 'ended']
