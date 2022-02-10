from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Bets, Event


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'sector', 'password1', 'password2']


class AddBetForm(ModelForm):
    class Meta:
        model = Bets
        fields = ['bet_name', 'ended']


class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_description', 'event_date', 'max_attendees']
