from django.db import models
from django.contrib.auth.models import AbstractUser


# Klaxcoin
class Klaxcoin(models.Model):
    value: models.DecimalField(max_digits=12, decimal_places=2)


# User
class User(AbstractUser):
    id_user = models.AutoField(primary_key=True, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    sector = (
        ('INFO', 'Informatique'),
        ('PHOT', 'Photonique'),
        ('SNUM', 'Systèmes numériques'),
        ('IMR', 'IMR')
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    klax_coins = models.OneToOneField(
        Klaxcoin,
        on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Bets(models.Model):
    id_bet = models.AutoField(primary_key=True, unique=True)
    bet_name = models.CharField(max_length=256, unique=True)

    win_rate = models.DecimalField(max_digits=4, decimal_places=2)
    win_vote = models.IntegerField()
    win_gains = models.OneToOneField('Klaxcoin', on_delete=models.CASCADE, related_name='wKlaxcoin')

    draw_rate = models.DecimalField(max_digits=4, decimal_places=2)
    draw_vote = models.IntegerField()
    draw_gains = models.OneToOneField('Klaxcoin', on_delete=models.CASCADE, related_name='dKlaxcoin')

    lose_rate = models.DecimalField(max_digits=4, decimal_places=2)
    lose_vote = models.IntegerField()
    lose_gains = models.OneToOneField('Klaxcoin', on_delete=models.CASCADE, related_name='lKlaxcoin')

    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField()


class StoreBets(models.Model):
    bet_id = models.ForeignKey('Bets', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    choice = (
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Lose')
    )
    gains = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    is_combined = models.BooleanField()
    id_combined = models.IntegerField(default=int(0))   # refers to the lower combined bet, if not itself
