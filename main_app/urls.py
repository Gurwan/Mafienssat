from django.urls import path
from main_app import views

urlpatterns = [
        # Unregister
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),

        # Betklax
    path("home_betKlax/", views.homeBetKlax, name="homeBetKlax"),
    path("home_betKlax/betKlax/", views.betKlax, name="betKlax"),
    path("home_betKlax/ratingRecalculation", views.ratingRecalculation, name="ratingRecalculation"),
    path('home_betKlax/makeBetW', views.makeBetW, name='makeBetW'),
    path('home_betKlax/makeBetL', views.makeBetL, name='makeBetL'),
    path("home_betKlax/myBets/", views.myBets, name="myBets"),
    path("home_betKlax/addGains", views.addGains, name="addGains"),
    path("home_betKlax/finalizeBet", views.finalizeBet, name="finalizeBet"),

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
    path("home_allos/", views.homeAllos, name="homeAllos"),
    path("home_allos/allos/", views.allos, name="allos"),
    path("home_allos/myAllos/", views.myAllos, name="myAllos"),
    path("home_allos/buyAllos", views.buyAllos, name="buyAllos"),
    path("home_allos/sendAllo", views.sendAllo, name="sendAllo"),
    path("home_allos/buyAlloTicket", views.buyAlloTicket, name="buyAlloTicket"),
    path("home_allos/alloRegistration/<int:id_allo>/", views.alloRegistration, name="alloRegistration"),
    path("home_allos/takeOverAllo", views.takeOverAllo, name="takeOverAllo"),
    path("home_allos/dontTakeOverAllo", views.dontTakeOverAllo, name="dontTakeOverAllo"),

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
