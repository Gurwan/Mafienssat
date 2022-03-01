from django.urls import path
from main_app import views

urlpatterns = [
        # Unregister
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),

        # Betklax
    path("betKlax/", views.betKlax, name="betKlax"),
    path("ratingRecalculation", views.ratingRecalculation, name="ratingRecalculation"),
    path('makeBetW', views.makeBetW, name='makeBetW'),
    path('makeBetL', views.makeBetL, name='makeBetL'),
    path("myBets/", views.myBets, name="myBets"),
    path("addGains", views.addGains, name="addGains"),
    path("finalizeBet", views.finalizeBet, name="finalizeBet"),

        # Event
    path("event/", views.event, name="event"),
    path("event/<int:id_event>/", views.eventHTML, name="eventHTML"),
    path("eventRegistration", views.eventRegistration, name="eventRegistration"),
    path("eventDeregistration", views.eventDeregistration, name="eventDeregistration"),

        # Liste
    path("liste/", views.liste, name="liste"),

        # Klaxment
    path("klaxment/", views.klaxment, name="klaxment"),

        # Goals
    path("goals/", views.goals, name="goals"),

        # Allos
    path("allos/", views.allos, name="allos"),
    path("myAllos/", views.myAllos, name="myAllos"),
    path("byAllos", views.buyAllos, name="byAllos"),
    path("sendAllo", views.sendAllo, name="sendAllo"),
    path("buyAlloTicket", views.buyAlloTicket, name="buyAlloTicket"),
    path("alloRegistration/<int:id_allo>/", views.alloRegistration, name="alloRegistration"),
    path("takeOverAllo", views.takeOverAllo, name="takeOverAllo"),
    path("dontTakeOverAllo", views.dontTakeOverAllo, name="dontTakeOverAllo"),

        # Footer
    path("partners/", views.partners, name="partners"),
    path("credits/", views.ourCredits, name="credits"),
    path("values/", views.ourValues, name="values"),
    path("promises/", views.promises, name="promises"),

        # Staff
    path("staff/", views.staff, name="staff"),
    path("staff/betCreator/", views.betCreator, name="betCreator"),
    path("staff/eventCreator/", views.eventCreator, name="eventCreator"),
    path("staff/alloCreator/", views.alloCreator, name="alloCreator"),
    path("staff/alloRequested/", views.alloRequested, name="alloRequested")
]
