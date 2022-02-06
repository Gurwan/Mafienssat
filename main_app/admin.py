from django.contrib import admin

# Register your models here.
from .models import User, Bets, StoreBets

admin.site.register(User)
admin.site.register(Bets)
admin.site.register(StoreBets)
