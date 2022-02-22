from django.db import models
from django.contrib.auth.models import AbstractUser


# User
class User(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    SECTOR = (
        ('INFO', 'Informatique'),
        ('PHOT', 'Photonique'),
        ('SNUM', 'Systèmes numériques'),
        ('IMR', 'IMR')
    )
    sector = models.CharField(max_length=4, choices=SECTOR, blank=True, help_text='Donne moi ta filière bro')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    klax_coins = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Bets(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    bet_name = models.CharField(max_length=256, unique=True)

    win_rate = models.DecimalField(max_digits=4, decimal_places=2, default=2.00)
    win_vote = models.IntegerField(default=0)
    win_gains = models.DecimalField(max_digits=12, decimal_places=2, default=1.00)

    lose_rate = models.DecimalField(max_digits=4, decimal_places=2, default=2.00)
    lose_vote = models.IntegerField(default=0)
    lose_gains = models.DecimalField(max_digits=12, decimal_places=2, default=1.00)

    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')


class StoreBets(models.Model):
    bet_id = models.ForeignKey('Bets', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    RESULT = (
        ('W', 'Win'),
        ('L', 'Lose')
    )
    result = models.CharField(max_length=1, choices=RESULT, blank=True, help_text='Which result for the bet')
    gains = models.DecimalField(max_digits=12, decimal_places=2, default=1.00)
    created = models.DateTimeField(auto_now_add=True)
    bet_rate = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    blocked_bet = models.BooleanField(default=False)


class Event(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    event_name = models.CharField(max_length=256, unique=True)
    event_description = models.CharField(max_length=1024)
    TYPE = (
        ('A', 'Annonce'),
        ('C', 'Chasse au trésor'),
        ('E', 'E-Sport'),
        ('J', 'Jeux'),
        ('P', 'Prévention'),
        ('K', 'Ker\'mess'),
        ('So', 'Soirée'),
        ('Sp', 'Sport'),
        ('T', 'Tournoi')
    )
    event_type = models.CharField(max_length=2, choices=TYPE, blank=True, help_text='Which type of event')
    event_date = models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')
    attendees_number = models.IntegerField(default=0)
    max_attendees = models.IntegerField(null=True)
    associated_bet = models.BooleanField(default=False)


class EventRegistration(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)


class Allos(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=1.00)


class AllosRegistration(models.Model):
    allo_id = models.ForeignKey('Allos', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateField(help_text='YYYY-MM-DD HH:MM:SS')
    take_over = models.BooleanField(default=False)
    made = models.BooleanField(default=False)
7