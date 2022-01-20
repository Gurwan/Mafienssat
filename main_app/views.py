from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Ca marche pas contacte Mafienssat sur insta et viens gueuler en mp bg')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'L\'utilisateur n\'existe pas ou tu t\'es trompé de mot de passe')


    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    players = User.objects.all() #va chercher tous les utilisateurs du site
    data = {'players': players}
    return render(request, 'home.html',data)
# Create your views here.
