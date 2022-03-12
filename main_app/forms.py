from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Bets, Event, Allos, AllosRegistration


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'sector', 'password1', 'password2']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'username': 'Pseudo',
            'sector': 'Filière',
            'password1': 'Mot de passe',
            'password2': 'Confirmer le mot de passe ',
        }


class AddBetForm(ModelForm):
    class Meta:
        model = Bets
        fields = ['bet_name', 'ended', 'win_name', 'lose_name']
        labels = {
            'bet_name': 'Nom du pari',
            'ended': 'Date et heure de fin pour parier au format YYYY-MM-DD HH:MM:SS',
            'win_name': 'Nom du bouton de victoire du pari (par défaut Oui)',
            'lose_name': 'Nom du bouton de défaite du pari (par défaut Non)'
        }


class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_description', 'event_date', 'max_attendees', 'associated_bet', 'associated_html']
        labels = {
            'event_name': 'Nom de l\'event',
            'event_type': 'Type de l\'event',
            'event_description': 'Description succincte de l\'event',
            'event_date': 'Date et heure de l\'event au format YYYY-MM-DD HH:MM:SS',
            'max_attendees': 'Nombre maximum de participant 0 si pas de jauge',
            'associated_bet': 'À cocher s\'il y a un pari associé',
            'associated_html': 'À cocher s\'il y a une page associée à cet event'
        }


class AlloAdminForm(ModelForm):
    class Meta:
        model = Allos
        fields = ['allo_type', 'description', 'cost', 'start_date', 'end_date']
        labels = {
            'allo_type': 'Type de allo à proposer',
            'description': 'Description succincte du allo',
            'cost': 'Coût en klaxcoins du allo',
            'start_date': 'Date et heure de début de disponibilité au format YYYY-MM-DD HH:MM:SS',
            'end_date': 'Date et heure de fin de disponibilité au format YYYY-MM-DD HH:MM:SS'
        }


class AlloForm(ModelForm):
    class Meta:
        model = AllosRegistration
        fields = ['date']
