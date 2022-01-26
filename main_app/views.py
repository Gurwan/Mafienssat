from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Ca marche pas contacte Mafienssat sur insta et viens gueuler en mp bg')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'L\'utilisateur n\'existe pas ou tu t\'es trompé de mot de passe')


    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création de l\'utilisateur')

    return render(request, 'register.html', {'form': form})


def home(request):
    players = User.objects.all() #va chercher tous les utilisateurs du site
    data = {'players': players}
    return render(request, 'home.html',data)
# Create your views here.
