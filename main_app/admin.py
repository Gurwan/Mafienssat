from django.contrib import admin

# Register your models here.
from .models import User, Bets, StoreBets, Event, EventsRegistration, Allos, AllosRegistration, AllosUserCounters

admin.site.register(User)
admin.site.register(Bets)
admin.site.register(StoreBets)
admin.site.register(Event)
admin.site.register(EventsRegistration)
admin.site.register(Allos)
admin.site.register(AllosRegistration)
admin.site.register(AllosUserCounters)
