from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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


def makeBetW(request):
    print("win Bet")
    current_user = request.user
    if current_user is not None:
        primary_key = request.POST["id"] if request.POST["id"] is not None else ''
        print("found primary key")
        bet = Bets.objects.get(pk=int(primary_key))
        myBet = StoreBets()
        myBet.RESULT = 'W'
        myBet.bet_id = bet.id
        myBet.user_id = current_user
        myBet.save()

    else:
        messages.error(request, "Il faut te connecter pour parier")

    return redirect('betKlax')


def makeBetL(request):
    if request.user is not None:
        r = request.POST.get('makeBetW') if request.POST.get('makeBetW') is not None else ''
        if r != '':
            bet = Bets.objects.get(bet_name__exact=r)
            myBet = StoreBets()
            myBet.RESULT = 'L'
            myBet.bet_id = bet.id
            myBet.user_id = request.user.id
            myBet.save()
        else:
            messages.error(request, "Aucun pari sélectionné")

    else:
        messages.error(request, "Il faut te connecter pour parier")

    return render('betKlax')


def myBets(request):
    current_user = request.user
    if current_user is not None:
        bets = StoreBets.objects.filter(pk=current_user.id)
        return render(request, 'myBetKlax.html', {'mybets': bets})
    else:
        messages.error(request, "Connecte toi")


def betKlax(request):
    # show all bets
    bets = Bets.objects.all()

    if request.POST.get('makeBetW'):
        makeBetW(request)
    # add a new bet
 #   form = AddBetForm()
    #   if request.method == 'POST':
    #    form = AddBetForm(request.POST)
    #    if form.is_valid():
    #        bet = form.save(commit=False)
    #        bet.save()
    #    else:
    #        messages.error(request, 'Erreur lors de la création du paris')
    return render(request, 'betKlax.html', {'bets': bets})
    #return render(request, 'betKlax.html', {'form': form, 'bets': bets})

