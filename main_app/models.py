import uuid

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
    klax_coins = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Bets(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    bet_name = models.CharField(max_length=256, unique=True)

    win_rate = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    win_vote = models.IntegerField(default=0)
    win_gains = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    draw_rate = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    draw_vote = models.IntegerField(default=0)
    draw_gains = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    lose_rate = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    lose_vote = models.IntegerField(default=0)
    lose_gains = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField()


class StoreBets(models.Model):
    bet_id = models.ForeignKey('Bets', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    RESULT = (
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Lose')
    )
    result = models.CharField(max_length=1, choices=RESULT, blank=True, help_text='Which result for the bet')
    gains = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    is_combined = models.BooleanField(default=False)
    id_combined = models.IntegerField(null=True)   # refers to the lower combined bet, if not itself
