from django.db import models
from django.contrib.auth.models import AbstractUser

class Klaxcoin(models.Model):
    number : models.DecimalField()

# Create your models here.
class User(AbstractUser):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=35)
    email = models.EmailField(unique=True, null=True)
    filiere = (
        ('INFO', 'Informatique'),
        ('PHOT', 'Photonique'),
        ('SNUM', 'Systèmes numériques'),
        ('IMR', 'IMR')
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    klaxs = models.OneToOneField(
        Klaxcoin, 
        on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

# class Event(models.Model):
   # users = models.ManyToManyField(to)

