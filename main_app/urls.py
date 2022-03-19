from django.urls import path
from main_app import views

urlpatterns = [
        # Unregister
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

        # Betklax
    path("home_betKlax/", views.homeBetKlax, name="homeBetKlax"),
    path("home_betKlax/betKlax/", views.betKlax, name="betKlax"),
    path("home_betKlax/ratingRecalculation", views.ratingRecalculation, name="ratingRecalculation"),
    path('home_betKlax/makeBetW/<int:id_bet>/', views.makeBetW, name='makeBetW'),
    path('home_betKlax/makeBetL/<int:id_bet>/', views.makeBetL, name='makeBetL'),
    path("home_betKlax/myBets/", views.myBets, name="myBets"),
    path("home_betKlax/addGains/[<int:id_bet>, <int:gains>]", views.addGains, name="addGains"),
    path("home_betKlax/finalizeBet/<int:id_bet>", views.finalizeBet, name="finalizeBet"),

        # Event
    path("event/", views.event, name="event"),
    path("event/eventRegistration/<int:event_id>/", views.eventRegistration, name="eventRegistration"),
    path("event/eventUnregistration/<int:event_id>/", views.eventUnregistration, name="eventUnregistration"),
    path("event/Chasse_au_tresor/", views.Chasse, name="Chasse"),
    path("event/Tournois_des_foufous/", views.Tournois, name="Tournois"),

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
    path("home_allos/myAllos/removeAllo/<int:id_allo>/", views.removeAllo, name="removeAllo"),
    path("home_allos/sendAllo/[<str:date>, <str:time>, <int:allo_id>]/", views.sendAllo, name="sendAllo"),
    path("home_allos/alloRegistration/<int:id_allo>/", views.alloRegistration, name="alloRegistration"),

        # Footer
    path("partners/", views.partners, name="partners"),
    path("thanks/", views.ourThanks, name="thanks"),
    path("values/", views.ourValues, name="values"),
    path("promises/", views.promises, name="promises"),

        # Staff
    path("staff/", views.staff, name="staff"),
    path("staff/users", views.suUsers, name="suUsers"),
    path("staff/betCreator/", views.betCreator, name="betCreator"),
    path("staff/betCreator/setVisbleBet/<int:id_bet>/", views.setVisibleBet, name="setVisibleBet"),
    path("staff/eventCreator/", views.eventCreator, name="eventCreator"),
    path("staff/eventCreator/setVisbleEvent/<int:id_event>/", views.setVisibleEvent, name="setVisibleEvent"),
    path("staff/alloCreator/", views.alloCreator, name="alloCreator"),
    path("staff/alloCreator/setVisbleAllo/<int:id_allo>/", views.setVisibleAllo, name="setVisibleAllo"),
    path("staff/alloRequested/", views.alloRequested, name="alloRequested"),
    path("staff/alloRequested/finalizeAllo/<int:id_finalized_allo>/", views.finalizeAllo, name="finalizeAllo"),
    path("staff/alloRequested/alloEmailConfirmation/<int:id_allo>/", views.alloEmailConfirmation, name="alloEmailConfirmation"),
    path("staff/alloRequested/alloEmailConfirmation/sendAlloEmailConfirmation/[<str:date>, <str:time>, <int:allo_id>]/", views.sendAlloEmailConfirmation, name="sendAlloEmailConfirmation"),

        # SuperUser
    path("staff/betSuperUser/", views.suBets, name="suBets"),
    path("staff/betSuperUser/suCheckBet/<int:id_bet>/", views.suCheckBet, name="suCheckBet"),
    path("staff/betSuperUser/closeBet/<int:id_bet>/", views.closeBet, name="closeBet"),
    path("staff/betSuperUser/deleteBet/<int:id_bet>/", views.deleteBet, name="deleteBet"),
    path("staff/betSuperUser/sendBetsKalxcoins/[<int:id_bet>, <str:result_bet>]/", views.sendBetsKalxcoins, name="sendBetsKalxcoins"),
    path("staff/eventSuperUser/", views.suEvents, name="suEvents"),
    path("staff/betSuperUser/suCheckEvent/<int:id_event>/", views.suCheckEvent, name="suCheckEvent"),
    path("staff/eventSuperUser/closeEvent/<int:id_event>/", views.closeEvent, name="closeEvent"),
    path("staff/betSuperUser/deleteEvent/<int:id_event>/", views.deleteEvent, name="deleteEvent"),
    path("staff/alloSuperUser/", views.suAllos, name="suAllos"),
    path("staff/alloSuperUser/closeAllo/<int:id_allo>/", views.closeAllo, name="closeAllo"),
    path("staff/betSuperUser/deleteAllo/<int:id_allo>/", views.deleteAllo, name="deleteAllo"),
]
