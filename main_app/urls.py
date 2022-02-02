from django.urls import path
from main_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("betKlax/", views.betKlax, name="betKlax")
]