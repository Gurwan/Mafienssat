from django.urls import path
from main_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),

    path("betKlax/", views.betKlax, name="betKlax"),

    path("ratingRecalculation", views.ratingRecalculation, name="ratingRecalculation"),
    path('makeBetW', views.makeBetW, name='makeBetW'),
    path('makeBetL', views.makeBetL, name='makeBetL'),
    path("myBets/", views.myBets, name="myBets"),
    path("addGains", views.addGains, name="addGains"),
    path("finalizeBet", views.finalizeBet, name="finalizeBet"),

    path("event/", views.event, name="event"),
    path("eventRegistration", views.eventRegistration, name="eventRegistration"),

    path("liste/", views.liste, name="liste"),

    path("klaxment/", views.klaxment, name="klaxment"),

    path("goals/", views.goals, name="goals"),

    path("allos/", views.allos, name="allos"),
    path("sendAllo", views.sendAllo, name="sendAllo"),
    path("alloRegistration/<int:id_allo>/", views.alloRegistration, name="alloRegistration"),

    path("staff/", views.staff, name="staff"),
    path("staff/betCreator/", views.addBet, name="betCreator"),
    path("staff/eventCreator/", views.addEvent, name="eventCreator"),
    path("staff/alloCreator/", views.alloCreator, name="alloCreator"),
]
