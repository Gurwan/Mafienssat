from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import User, Bets, StoreBets
from .forms import UserForm, AddBetForm


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Ca marche pas contacte Mafienssat sur insta et viens gueuler en mp bg')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
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
    players = User.objects.all()  # va chercher tous les utilisateurs du site
    data = {'players': players}

    return render(request, 'home.html', data)


def addBet(request):
    if request.user.is_staff:
        betform = AddBetForm()
        if request.method == 'POST':
            betform = AddBetForm(request.POST)
            if betform.is_valid():
                bet = betform.save(commit=False)
                bet.save()
            else:
                messages.error(request, 'Erreur lors de la création du paris')
        return render(request, 'betCreator.html', {'betform': betform})
    else:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def makeBetW(request):

    current_user = request.user
    if current_user is not None:
        primary_key = request.POST['bet'] if request.POST['bet'] is not None else messages.error(request, "Votre demande ne peut aboutir actuellement, si cella perciste, veuollez contacter un admin du site")
        gains = request.POST['gains'] if request.POST['gains'] is not None else messages.error(request, "Votre demande ne peut aboutir actuellement, si cella perciste, veuollez contacter un admin du site")
        myBet = StoreBets()
        myBet.bet_name = Bets.objects.get(id=primary_key).bet_name
        myBet.result = 'W'
        myBet.gains = gains
        myBet.bet_id = Bets.objects.get(id=primary_key)
        myBet.user_id = current_user
        myBet.save()

    else:
        messages.error(request, "Il faut te connecter pour parier")

    return redirect('betKlax')


def makeBetL(request):

    current_user = request.user
    if current_user is not None:
        primary_key = request.POST['bet'] if request.POST['bet'] is not None else messages.error(request, "Votre demande ne peut aboutir actuellement, si cella perciste, veuollez contacter un admin du site")
        gains = request.POST['gains'] if request.POST['gains'] is not None else messages.error(request, "Votre demande ne peut aboutir actuellement, si cella perciste, veuollez contacter un admin du site")
        myBet = StoreBets()
        myBet.bet_name = Bets.objects.get(id=primary_key).bet_name
        myBet.result = 'L'
        myBet.gains = gains
        myBet.bet_id = Bets.objects.get(id=primary_key)
        myBet.user_id = current_user
        myBet.save()

    else:
        messages.error(request, "Il faut te connecter pour parier")

    return redirect('betKlax')


def myBets(request):

    current_user = request.user
    if current_user is not None:
        mybets = StoreBets.objects.all().filter(user_id_id=current_user.id)
        return render(request, 'myBetKlax.html', {'mybets': mybets})
    else:
        messages.error(request, "Connecte toi")


def betKlax(request):

    current_user = request.user
    if current_user is not None: # if the user is logged he see the remaining bets
        bets_done = StoreBets.objects.filter(user_id_id=current_user.id)
        bets = Bets.objects.all()
        #for bet in bets_done:
        #    bets = bets.exclude(pk=bet.bet_id_id)

    else:   # show all bets
        bets = Bets.objects.all()

    return render(request, 'betKlax.html', {'bets': bets})


def event(request):
    return render(request, 'event.html')

def liste(request):
    return render(request, 'liste.html')
