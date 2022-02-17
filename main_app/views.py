from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from decimal import *
from .models import User, Bets, StoreBets, Event, Registrations
from .forms import UserForm, AddBetForm, AddEventForm


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
        bets = Bets.objects.all()
        return render(request, 'betCreator.html', {'betform': betform, 'bets': bets})
    else:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def ratingRecalculation(request):
    bet_id = request.POST['bet']
    bet = Bets.objects.all().get(pk=bet_id)
    if bet is not None:
        w_gains = float(bet.win_gains) if bet.win_gains > Decimal(0) else Decimal(1)
        l_gains = float(bet.lose_gains) if bet.lose_gains > Decimal(0) else Decimal(1)
        w_rate = (w_gains + l_gains)/w_gains
        l_rate = (w_gains + l_gains)/l_gains
        bet.win_rate = Decimal(w_rate)
        bet.lose_rate = Decimal(l_rate)
        bet.save()

        name = request.POST['name']
        if name is not None:
            return redirect(name)
        else:
            return redirect('home')
    else:
        messages.error(request, "Problème rencontré lors du recalcul des cotes")


def makeBetW(request):
    if request.user is not None:
        current_user = User.objects.get(pk=request.user.id)
        primary_key = request.POST['bet'] if request.POST['bet'] is not None else messages.error(request,
                                                                                                 "Votre demande ne peut aboutir actuellement, si cella perciste, veuollez contacter un admin du site")

        cdt = StoreBets.objects.filter(bet_id_id=primary_key).filter(user_id_id=current_user)
        if cdt.count() == 0:
            if current_user.klax_coins > 0:

                current_user.klax_coins -= 1
                current_user.save()

                myBet = StoreBets()
                myBet.result = 'W'
                myBet.gains = 1
                myBet.bet_id = Bets.objects.get(id=primary_key)
                myBet.user_id = request.user
                myBet.bet_id.win_gains += 1
                myBet.bet_id.win_vote += 1
                myBet.save()
            else:
                messages.error(request, "Tu n\'as pas asser de klax_coins espèce de rat")
        else:
            messages.error(request, "Tu as déja parié sur ce pari")
    else:
        messages.error(request, "Il faut te connecter pour parier")

    return redirect('betKlax')


def makeBetL(request):
    current_user = User.objects.get(pk=request.user.id)
    if current_user is not None:
        primary_key = request.POST['bet'] if request.POST['bet'] is not None else messages.error(request,
                                                                                                 "Votre demande ne peut aboutir actuellement, si cella perciste, veuollez contacter un admin du site")
        cdt = StoreBets.objects.filter(bet_id_id=primary_key).filter(user_id_id=current_user)
        if cdt.count() == 0:
            if current_user.klax_coins > 0:
                current_user.klax_coins -= 1
                current_user.save()

                myBet = StoreBets()
                myBet.result = 'L'
                myBet.gains = 1
                myBet.bet_id = Bets.objects.get(id=primary_key)
                myBet.user_id = request.user
                myBet.bet_id.lose_gains += 1
                myBet.bet_id.lose_vote += 1
                myBet.save()
            else:
                messages.error(request, "Tu n\'as pas asser de klax_coins espèce de rat")
        else:
            messages.error(request, "Tu as déja parié sur ce pari")
    else:
        messages.error(request, "Il faut te connecter pour parier")

    return redirect("betKlax")


def myBets(request):
    current_user = request.user
    if current_user is not None:
        finalizedBets = StoreBets.objects.all().filter(user_id_id=current_user.id, blocked_bet=True)
        finalId = []
        for b in finalizedBets:
            finalId.append(b.bet_id.id)
        mybets = StoreBets.objects.all().filter(user_id_id=current_user.id).exclude(bet_id_id__in=finalId)
        user = User.objects.get(pk=current_user.id)
        # todo ajouter la requête permettant de récupérer les combinés dans tab 2D

        return render(request, 'myBetKlax.html', {'mybets': mybets, 'finalizedBets': finalizedBets, 'user': user})
    else:
        messages.error(request, "Connecte toi")


def addGains(request):
    current_user = User.objects.get(pk=request.user.id)
    if current_user is not None:
        bet_id = request.POST['bet']
        gains = request.POST['gains']
        print(current_user.id)
        if current_user.klax_coins >= Decimal(gains):
            print(bet_id)
            bet = StoreBets.objects.all().get(user_id_id=current_user.id, bet_id_id=bet_id)
            bet.gains += Decimal(gains)
            if bet.result == 'W':
                bet.bet_id.win_gains += Decimal(gains)
            else:
                bet.bet_id.lose_gains += Decimal(gains)
            bet.save()

            current_user.klax_coins -= Decimal(gains)
            current_user.save()
        else:
            messages.error(request, "Tu n'as pas asser de KlaxCoins espèce de rat")
    else:
        messages.error(request, "Il faut être connecté pour acceder à cette page")
    return redirect("myBets")


def finalizeBet(request):
    current_user = User.objects.get(pk=request.user.id)
    if current_user is not None:
        bet_id = request.POST['bet']
        gains = request.POST['gains'] if request.POST['gains'] is not "" else Decimal(0)
        print(gains)
        if current_user.klax_coins >= Decimal(gains):
            if bet_id is not None:
                bet = StoreBets.objects.get(bet_id_id=bet_id, user_id_id=current_user.id)
                if bet is not None:
                    if gains > 0:
                        current_user.klax_coins -= Decimal(gains)
                        current_user.save()
                        bet.gains += Decimal(gains)

                    if bet.result == 'W':
                        bet.bet_id.win_gains += Decimal(gains)
                        bet.bet_rate = bet.bet_id.win_rate
                    else:
                        bet.bet_id.lose_gains += Decimal(gains)
                        bet.bet_rate = bet.bet_id.lose_rate
                    bet.blocked_bet = True
                    bet.save()
            else:
                messages.error(request, "Contacte les admins si le problème perciste après un refresh de la page")
        else:
            messages.error(request, "Tu n'as pas assez de KlaxCoins espèce de rat")
    else:
        messages.error(request, "Tu dois être connecté pour accéder à cette page")

    return redirect("myBets")


def betKlax(request):
    current_user = request.user
    if current_user is not None:  # if the user is logged he see the remaining bets
        bets_done = StoreBets.objects.filter(user_id_id=current_user.id)
        bet = []
        for b in bets_done:
            bet.append(b.bet_id_id)
        bets = Bets.objects.exclude(id__in=bet)
        user = User.objects.get(pk=current_user.id)

    else:  # show all bets
        bets = Bets.objects.all()
        user = None

    return render(request, 'betKlax.html', {'bets': bets, 'user': user})


def addEvent(request):
    if request.user.is_staff:
        eventform = AddEventForm()
        if request.method == 'POST':
            eventform = AddEventForm(request.POST)
            if eventform.is_valid():
                event = eventform.save(commit=False)
                event.save()
            else:
                messages.error(request, 'Erreur lors de la création d\'un événement')
        events = Event.objects.all()
        return render(request, 'eventCreator.html', {'eventform': eventform, 'events': events})
    else:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def event(request):
    return render(request, 'event.html')


def liste(request):
    return render(request, 'liste.html')


def klaxment(request):
    userList = User.objects.all().order_by('-klax_coins')  # va chercher tous les utilisateurs du site
    data = {'userList': userList}
    return render(request, 'klaxment.html', data)
