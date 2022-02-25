from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from decimal import *
from datetime import datetime
from .models import User, Bets, StoreBets, Event, EventRegistration, AllosRegistration, Allos
from .forms import UserForm, AddBetForm, AddEventForm, AlloAdminForm, AlloForm


def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Ca marche pas contacte Mafienssat sur insta et viens gueuler en mp bg')

        user = authenticate(request, email=email, password=password)

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
        return render(request, 'bets/betCreator.html', {'betform': betform, 'bets': bets})
    else:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def ratingRecalculation(request):
    bet_id = request.POST['bet']
    bet = Bets.objects.all().get(pk=bet_id)

    if bet is not None:
        w_gains = float(bet.win_gains) + float(1)
        l_gains = float(bet.lose_gains) + float(1)
        print(w_gains, l_gains)

        w_rate = (w_gains + l_gains)/w_gains
        l_rate = (w_gains + l_gains)/l_gains
        bet.win_rate = Decimal(w_rate)
        bet.lose_rate = Decimal(l_rate)
        bet.save()
        print(w_rate, l_rate)
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

                bet = Bets.objects.get(id=primary_key)
                bet.win_gains += 1
                bet.win_vote += 1
                bet.save()

                myBet = StoreBets()
                myBet.result = 'W'
                myBet.gains = 1
                myBet.bet_id = bet
                myBet.user_id = request.user
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

                bet = Bets.objects.get(id=primary_key)
                bet.lose_gains += 1
                bet.lose_vote += 1
                bet.save()

                myBet = StoreBets()
                myBet.result = 'L'
                myBet.gains = 1
                myBet.bet_id = bet
                myBet.user_id = request.user
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

        return render(request, 'bets/myBetKlax.html', {'mybets': mybets, 'finalizedBets': finalizedBets, 'user': user})
    else:
        messages.error(request, "Connecte toi")


def addGains(request):
    current_user = User.objects.get(pk=request.user.id)
    if current_user is not None:
        bet_id = request.POST['bet']
        gains = request.POST['gains']
        if current_user.klax_coins >= Decimal(gains):
            bet = StoreBets.objects.get(user_id_id=current_user.id, bet_id_id=bet_id)
            bet.gains += Decimal(gains)
            if bet.result == 'W':
                bet.bet_id.win_gains += Decimal(gains)
                print(bet.bet_id.win_gains)
            elif bet.result == 'L':
                bet.bet_id.lose_gains += Decimal(gains)
                print(bet.bet_id.lose_gains)
            else:
                messages.error(request, "Le résultat du pari est inconnu")
            bet.bet_id.save()
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
        gains = request.POST['gains'] if request.POST['gains'] != "" else Decimal(0)
        print(gains)
        if current_user.klax_coins >= Decimal(gains):
            if bet_id is not None:
                bet = StoreBets.objects.get(bet_id_id=bet_id, user_id_id=current_user.id)
                if bet is not None:
                    if Decimal(gains) > Decimal(0):
                        current_user.klax_coins -= Decimal(gains)
                        current_user.save()
                        bet.gains += Decimal(gains)

                    if bet.result == 'W':
                        bet.bet_id.win_gains += Decimal(gains)
                        bet.bet_rate = bet.bet_id.win_rate
                        print("finalize w_g: ", bet.bet_id.win_gains)
                    elif bet.result == 'L':
                        bet.bet_id.lose_gains += Decimal(gains)
                        bet.bet_rate = bet.bet_id.lose_rate
                        print("finalize l_g: ", bet.bet_id.win_gains)
                    else:
                        messages.error(request, "Le résultat du pari est inconnu")

                    bet.blocked_bet = True
                    bet.bet_id.save()
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
        return redirect('myBets')

    else:  # show all bets
        bets = Bets.objects.all()
        user = None

    return render(request, 'bets/betKlax.html', {'bets': bets, 'user': user})


def addEvent(request):
    if request.user.is_staff:
        eventform = AddEventForm()
        if request.method == 'POST':
            eventform = AddEventForm(request.POST)
            if eventform.is_valid():
                eventf = eventform.save(commit=False)
                eventf.save()
            else:
                messages.error(request, 'Erreur lors de la création d\'un événement')
        events = Event.objects.all()
        return render(request, 'events/eventCreator.html', {'eventform': eventform, 'events': events})
    else:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def event(request):
    events = Event.objects.all()
    if request.user is not None:
        user = request.user
        registered_event = EventRegistration.objects.filter(user_id_id=user.id)
        reg_event_id = []
        for e in registered_event:
            reg_event_id.append(e.event_id.id)
        if reg_event_id:
            events = Event.objects.exclude(id__in=reg_event_id)
            registered_event = Event.objects.filter(id__in=reg_event_id)
    else:
        user = None
        registered_event = None
    data = {'events': events, 'user': user, 'registered': registered_event}

    return render(request, 'events/event.html', data)


def eventRegistration(request):

    if request.user is not None:
        if request.method == 'POST':
            event_id = request.POST['event']

            try:
                done = EventRegistration.objects.get(user_id_id=request.user.id, event_id_id=event_id)
            except EventRegistration.DoesNotExist:
                done = None

            if done is None and event_id is not None:
                this_event = Event.objects.get(pk=event_id)

                reg = EventRegistration()
                reg.event_id = this_event
                reg.user_id = request.user
                reg.save()

                if this_event.max_attendees != 0 and this_event.attendees_number < this_event.max_attendees:
                    this_event.attendees_number += 1
                    this_event.save()
                else:
                    messages.error(request, "Cet évènement est déja complet")
            else:
                messages.error(request, "Erreur lors de l'identification de l'évènement")
        else:
            messages.error(request, "Un problème est survenu lors de votre inscripion, veuillez réessayer et si cela persiste, veuillez contacter un admin")
    else:
        messages.error(request, "Vous devez être connecté pour vous inscrire à cet évènement")
    return redirect('event')


def eventDeregistration(request):

    if request.user is not None:
        if request.method == 'POST':
            event_id = request.POST['event']

            if event_id is not None:
                this_event = Event.objects.get(pk=event_id)
                this_event.attendees_number -= 1
                this_event.save()

                done = EventRegistration.objects.get(user_id_id=request.user.id, event_id_id=event_id)
                done.delete()
            else:
                messages.error(request, "Erreur lors de l'identification de l'évènement")
        else:
            messages.error(request, "Un problème est survenu lors de votre inscripion, veuillez réessayer et si cela persiste, veuillez contacter un admin")
    else:
        messages.error(request, "Vous devez être connecté pour vous inscrire à cet évènement")
    return redirect('event')


def liste(request):
    return render(request, 'nav_links/liste.html')


def klaxment(request):
    userList = User.objects.all().order_by('-klax_coins')  # va chercher tous les utilisateurs du site
    data = {'userList': userList}
    return render(request, 'nav_links/klaxment.html', data)


def allos(request):
    all_allos = Allos.objects.all()
    return render(request, 'allos/allos.html', {'allos': all_allos})


def sendAllo(request):
    if request.method == 'POST':
        date = request.POST['date'] + " " + request.POST['time'] + ":00"
        allo_id = request.POST['allo']
        if date is not None and allo_id is not None:
            selected_allo = Allos.objects.get(id=allo_id)

            user = User.objects.get(pk=request.user.id)
            if user is not None:
                allo = AllosRegistration()
                allo.user_id = user
                allo.allo_id = selected_allo
                allo.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                allo.save()
                return redirect('allos')
            else:
                messages.error(request, "Utilisateur non trouvé")
        else:
            messages.error(request, "Erreur lors de l\'envoie de ta demande")
    else:
        messages.error(request, "Erreur lors de l\'envoie de ta demande")


def alloCreator(request):
    form = AlloAdminForm()

    if request.method == 'POST':
        form = AlloAdminForm(request.POST)
        if form.is_valid():
            allo = form.save(commit=False)
            allo.save()
            return redirect('alloCreator')
        else:
            messages.error(request, "Erreur lors de la creation du allo")

    all_allos = Allos.objects.all()

    return render(request, 'allos/alloCreator.html', {'form': form, 'allos': all_allos})


def alloRegistration(request, id_allo):
    selected_allo = Allos.objects.get(pk=id_allo)

    return render(request, 'allos/alloRegistration.html', {'allo': selected_allo})


def alloRequested(request):
    all_request = AllosRegistration.objects.filter(made=False)
    return render(request, 'allos/alloRequested.html', {'allos': all_request})


def takeOverAllo(request):
    if request.method == 'POST':
        allo_id = request.POST['allo']
        allo = AllosRegistration.objects.get(id=allo_id)
        allo.take_over = True
        allo.save()
    redirect('alloRequested')


def dontTakeOverAllo(request):
    if request.method == 'POST':
        allo_id = request.POST['allo']
        allo = AllosRegistration.objects.get(id=allo_id)
        allo.take_over = False
        allo.save()
    redirect('alloRequested')


def staff(request):
    return render(request, 'staff.html')


def goals(request):
    return render(request, 'nav_links/goals.html')


def partners(request):
    return render(request, 'footers/partners.html')


def ourCredits(request):
    return render(request, 'footers/credits.html')


def promises(request):
    return render(request, 'footers/campaignPromises.html')


def ourValues(request):
    return render(request, 'footers/ourValues.html')
