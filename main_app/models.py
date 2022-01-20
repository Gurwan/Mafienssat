from django.db import models

class Klaxcoin(models.Model):
    number : models.DecimalField()

# Create your models here.
class User(models.Model):

    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=35)
    filiere = (
        ('INFO', 'Informatique'),
        ('PHOT', 'Photonique')
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    klaxs = models.OneToOneField(
        Klaxcoin, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


