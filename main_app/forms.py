from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Bets, Event, Allos, AllosRegistration


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'sector', 'password1', 'password2']
        labels = {
            'firstname' : 'Prénom',
            'lastname' : 'Nom',
            'username' : 'Pseudo',
            'sector' : 'Filière',
            'password1' : 'Mot de passe',
            'password2' : 'Confirmer le mot de passe ',
        }


class AddBetForm(ModelForm):
    class Meta:
        model = Bets
        fields = ['bet_name', 'ended']


class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_description', 'event_date', 'max_attendees', 'associated_bet']


class AlloAdminForm(ModelForm):
    class Meta:
        model = Allos
        fields = ['name', 'description', 'cost']


class AlloForm(ModelForm):
    class Meta:
        model = AllosRegistration
        fields = ['date']
