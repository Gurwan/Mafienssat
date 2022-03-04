from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from decimal import *
from datetime import datetime
from .models import User, Bets, StoreBets, Event, EventRegistration, AllosRegistration, Allos, AllosUserCounters
from .forms import UserForm, AddBetForm, AddEventForm, AlloAdminForm


def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

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
            allos_counters = AllosUserCounters(user_id=user)
            allos_counters.save()
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la création de l\'utilisateur')

    return render(request, 'register.html', {'form': form})


def home(request):
    players = User.objects.all()
    data = {'players': players}

    return render(request, 'home.html', data)


def homeBetKlax(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    return render(request, 'bets/homeBets.html', {'user': user})


def betKlax(request):
    try:
        bets_done = StoreBets.objects.filter(user_id_id=request.user.id)
        bet = []
        for b in bets_done:
            bet.append(b.bet_id_id)
        bets = Bets.objects.exclude(id__in=bet)
        user = User.objects.get(pk=request.user.id)

    except User.DoesNotExist:
        bets = Bets.objects.all()
        user = None

    return render(request, 'bets/betKlax.html', {'bets': bets, 'user': user})


def betCreator(request):
    try:
        user = User.objects.get(pk=request.user.id)
        betform = AddBetForm()
        if request.method == 'POST':
            betform = AddBetForm(request.POST)
            if betform.is_valid():
                bet = betform.save(commit=False)
                bet.save()
            else:
                messages.error(request, 'Erreur lors de la création du paris')

        bets = Bets.objects.all()

        return render(request, 'bets/betCreator.html', {'user': user, 'betform': betform, 'bets': bets})
    except User.DoesNotExist:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def ratingRecalculation(request):
    if request.method == 'POST':
        bet_id = request.POST['bet']
        try:
            bet = Bets.objects.all().get(pk=bet_id)

        except Bets.DoesNotExist:
            bet = None

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
            messages.error(request, "Pari non reconnu veuillez réessayer")
    else:
        messages.error(request, "Problème rencontré lors del'envoi de la requète")


def makeBetW(request, id_bet):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None
        messages.error(request, "Il faut te connecter pour parier")

    try:
        cdt = StoreBets.objects.filter(bet_id_id=id_bet).filter(user_id_id=user)
    except StoreBets.DoesNotExist:
        cdt = None

    if user is not None and cdt is not None:
        if cdt.count() == 0:
            if user.klax_coins > 0:

                user.klax_coins -= 1
                user.save()

                bet = Bets.objects.get(id=id_bet)
                bet.win_gains += 1
                bet.win_vote += 1
                bet.save()

                myBet = StoreBets()
                myBet.result = 'W'
                myBet.gains = 1
                myBet.bet_id = bet
                myBet.user_id = user
                myBet.save()

                return redirect("betKlax")
            else:
                messages.error(request, "Tu n\'as pas asser de klax_coins espèce de rat")
        else:
            messages.error(request, "Tu as déja parié sur ce pari")
    else:
        messages.error(request, "Erreur lors de l'envoie dela requète")


def makeBetL(request, id_bet):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None
        messages.error(request, "Il faut te connecter pour parier")

    try:
        cdt = StoreBets.objects.filter(bet_id_id=id_bet).filter(user_id_id=user)
    except StoreBets.DoesNotExist:
        cdt = None

    if user is not None and cdt is not None:
        if cdt.count() == 0:
            if user.klax_coins > 0:
                user.klax_coins -= 1
                user.save()

                bet = Bets.objects.get(id=id_bet)
                bet.lose_gains += 1
                bet.lose_vote += 1
                bet.save()

                myBet = StoreBets()
                myBet.result = 'L'
                myBet.gains = 1
                myBet.bet_id = bet
                myBet.user_id = user
                myBet.save()

                return redirect("betKlax")
            else:
                messages.error(request, "Tu n\'as pas asser de klax_coins espèce de rat")
        else:
            messages.error(request, "Tu as déja parié sur ce pari")
    else:
        messages.error(request, "Erreur lors de l'envoi de la requète")


def myBets(request):
    try:
        finalizedBets = StoreBets.objects.all().filter(user_id_id=request.user.id, blocked_bet=True)
    except User.DoesNotExist:
        finalizedBets = None

    finalId = []
    for b in finalizedBets:
        finalId.append(b.bet_id.id)

    try:
        mybets = StoreBets.objects.all().filter(user_id_id=request.user.id).exclude(bet_id_id__in=finalId)
    except StoreBets.DoesNotExist:
        mybets = None

    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if mybets is not None and user is not None:
        return render(request, 'bets/myBetKlax.html', {'mybets': mybets, 'finalizedBets': finalizedBets, 'user': user})


def addGains(request):
    try:
        current_user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        current_user = None

    if request.method == 'POST' and current_user is not None:
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

            return redirect("myBets")
        else:
            messages.error(request, "Tu n'as pas asser de KlaxCoins espèce de rat")
    else:
        messages.error(request, "Il faut être connecté pour acceder à cette page")


def finalizeBet(request):
    try:
        current_user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        current_user = None

    if current_user is not None:
        bet_id = request.POST['bet']
        gains = request.POST['gains'] if request.POST['gains'] != "" else Decimal(0)
        if current_user.klax_coins >= Decimal(gains):
            if bet_id is not None:
                try:
                    bet = StoreBets.objects.get(bet_id_id=bet_id, user_id_id=current_user.id)
                except StoreBets.DoesNotExist:
                    bet = None

                if bet is not None:
                    if Decimal(gains) > Decimal(0):
                        current_user.klax_coins -= Decimal(gains)
                        current_user.save()
                        bet.gains += Decimal(gains)

                    if bet.result == 'W':
                        bet.bet_id.win_gains += Decimal(gains)
                        bet.bet_rate = bet.bet_id.win_rate
                    elif bet.result == 'L':
                        bet.bet_id.lose_gains += Decimal(gains)
                        bet.bet_rate = bet.bet_id.lose_rate
                    else:
                        messages.error(request, "Le résultat du pari est inconnu")

                    bet.blocked_bet = True
                    bet.bet_id.save()
                    bet.save()

                    return redirect("myBets")
            else:
                messages.error(request, "Contacte les admins si le problème perciste après un refresh de la page")
        else:
            messages.error(request, "Tu n'as pas assez de KlaxCoins espèce de rat")
    else:
        messages.error(request, "Tu dois être connecté pour accéder à cette page")


def eventCreator(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        if user.is_staff:
            eventform = AddEventForm()
            if request.method == 'POST':
                eventform = AddEventForm(request.POST)
                if eventform.is_valid():
                    eventf = eventform.save(commit=False)
                    eventf.save()
                else:
                    messages.error(request, 'Erreur lors de la création d\'un événement')

            events = Event.objects.all()

            return render(request, 'events/eventCreator.html', {'user': user, 'eventform': eventform, 'events': events})
        else:
            messages.error(request, "Tu dois être membre du staff pour accéder à cette page")
    else:
        messages.error(request, "Vous devez être connecté pour accéder à cette page")


def event(request):
    events = Event.objects.all()
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    try:
        registered_event = EventRegistration.objects.filter(user_id_id=user.id)
    except EventRegistration.DoesNotExist:
        registered_event = None

    if registered_event is not None:
        reg_event_id = []
        for e in registered_event:
            reg_event_id.append(e.event_id.id)
        if reg_event_id:
            events = Event.objects.exclude(id__in=reg_event_id)
            registered_event = Event.objects.filter(id__in=reg_event_id)
    else:
        messages.error(request, "Erreur lors de l'envoie dea requète")

    return render(request, 'events/event.html', {'events': events, 'user': user, 'registered': registered_event})


def readFileForHTML(file_name):
    file = open(file_name)
    all_lines = file.read().splitlines()
    toReturn = []
    i = 0
    for line in all_lines:
        if line != '':
            line = line.split("**")
            toReturn.append({'index': str(i), 'infoClass': line[0], 'info': line[1]})
            i += 1

    return toReturn


def eventHTML(request, id_event):
    try:
        event_name = Event.objects.get(pk=id_event).event_name
    except Event.DoesNotExist:
        event_name = None

    if event_name is not None:

        infos = readFileForHTML("static/events/" + event_name + ".txt")

        return render(request, 'events/eventPresentation.html', {'event': event_name, 'infos': infos})
    else:
        messages.error(request, "Erreur lors de l'envoie de la requête")


def eventRegistration(request, event_id):

    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    try:
        done = EventRegistration.objects.get(user_id_id=user.id, event_id_id=event_id)
    except EventRegistration.DoesNotExist:
        done = None

    try:
        this_event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        this_event = None

    if done is None and user is not None and this_event is not None:

        if this_event.max_attendees != 0 and this_event.attendees_number < this_event.max_attendees:
            this_event.attendees_number += 1
            this_event.save()

            reg = EventRegistration()
            reg.event_id = this_event
            reg.user_id = user
            reg.save()

            return redirect('event')
        else:
            messages.error(request, "Cet évènement est déja complet")
    else:
        messages.error(request, "Erreur lors de l'identification de l'évènement")


def eventUnregistration(request, event_id):
    try:
        this_event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        this_event = None

    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if this_event is not None and user is not None:
        if event_id is not None:
            this_event.attendees_number -= 1
            this_event.save()

            done = EventRegistration.objects.get(user_id_id=request.user.id, event_id_id=event_id)
            done.delete()

            return redirect('event')
        else:
            messages.error(request, "Erreur lors de l'identification de l'évènement")
    else:
        messages.error(request, "Un problème est survenu lors de votre inscripion, veuillez réessayer et si cela persiste, veuillez contacter un admin")


def liste(request):
    return render(request, 'nav_links/liste.html')


def klaxment(request):
    userList = User.objects.filter(is_staff=False, is_superuser=False).order_by('-klax_coins')  # va chercher tous les utilisateurs du site
    data = {'userList': userList}
    return render(request, 'nav_links/klaxment.html', data)


def homeAllos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    return render(request, 'allos/homeAllos.html', {'user': user})


def allos(request):
    all_allos = Allos.objects.all()
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    return render(request, 'allos/allos.html', {'user': user, 'allos': all_allos})


def myAllos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        counter = AllosUserCounters.objects.get(user_id_id=user.id)
        my_allos = AllosRegistration.objects.filter(user_id_id=user.id)

        all_allos = Allos.objects.all()
        types = []
        for allo in all_allos:
            types.append(allo.allo_type)

        return render(request, 'allos/myAllos.html', {'user': user, 'counter': counter, 'allos': my_allos, 'allos_types': types})
    else:
        messages.error(request, "Vous devez être connecté")


def buyAllos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        if request.method == 'POST':
            allo_type = request.POST['allo']
            allo_cost = request.POST['cost']
            counter = AllosUserCounters.objects.get(user_id_id=user.id)
            if allo_type is not None and allo_cost is not None:
                if int(allo_cost) > 0:
                    if user.klax_coins >= Decimal(allo_cost):
                        user.klax_coins -= Decimal(allo_cost)
                        user.save()
                        addAlloCounter(allo_type, counter, 1)
                        counter.save()

                    else:
                        messages.error(request, "Tu n'as pas assez de klaxcoins")
                else:
                    addAlloCounter(allo_type, counter, 1)
                    counter.save()

                return redirect('myAllos')
            else:
                messages.error(request, "Erreur lors de l'envoie de la requete")
        else:
            messages.error(request, "Erreur lors de l'envoie de la requete")
    else:
        messages.error(request, "Vous devez être connecté")


def addAlloCounter(allo_type, counter, nb):
    if allo_type == "A":
        counter.biere += nb
    elif allo_type == "B":
        counter.gouter += nb
    elif allo_type == "C":
        counter.ptitdej += nb
    elif allo_type == "D":
        counter.menage += nb
    elif allo_type == "E":
        counter.car_wash += nb
    elif allo_type == "F":
        counter.klax += nb
    elif allo_type == "G":
        counter.cuisine += nb
    elif allo_type == "H":
        counter.courses += nb


def buyAlloTicket(request, allo_ticket_id):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None

    try:
        selected_allo = Allos.objects.get(id=allo_ticket_id)
    except Allos.DoesNotExist:
        selected_allo = None

    if user is not None and selected_allo is not None:

        counter = AllosUserCounters.objects.get(user_id=user)

        if user.klax_coins >= selected_allo.cost:
            user.klax_coins -= selected_allo.cost
            user.save()

            addAlloCounter(selected_allo.allo_type, counter, 1)
            counter.save()

            allowed = alloAllowed(selected_allo.allo_type, counter)

            return render(request, 'allos/alloRegistration.html', {'allo': selected_allo, 'allowed': allowed})
        else:
            messages.error(request, "Tu n'as pas assez de klaxcoins")
    else:
        messages.error(request, "Tu dois être connecté")


def sendAllo(request):
    try:
        user = User.objects.get(pk=request.user.id)
        if request.method == 'POST':
            date = request.POST['date'] + " " + request.POST['time'] + ":00"
            allo_id = request.POST['allo']
            if request.POST['date'] is not None and request.POST['time'] is not None and allo_id is not None:
                selected_allo = Allos.objects.get(id=allo_id)
                counter = AllosUserCounters.objects.get(user_id=request.user)
                if user is not None:
                    addAlloCounter(selected_allo.allo_type, counter, -1)
                    counter.save()

                    allo = AllosRegistration()
                    allo.user_id = user
                    allo.allo_id = selected_allo
                    allo.date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                    allo.save()

                else:
                    messages.error(request, "Utilisateur non trouvé")
            else:
                messages.error(request, "Erreur lors de l\'envoie de ta demande")
        else:
            messages.error(request, "Erreur lors de l\'envoie de ta demande")
    except User.DoesNotExist:
        user = None
        messages.error(request, "Vous devez être connecté")

    all_allos = Allos.objects.all()

    return render(request, 'allos/allos.html', {'user': user, 'allos': all_allos})


def alloCreator(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
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

        return render(request, 'allos/alloCreator.html', {'user': user, 'form': form, 'allos': all_allos})
    else:
        messages.error(request, "Vous devez être connecté")


def alloRegistration(request, id_allo):

    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        selected_allo = Allos.objects.get(pk=id_allo)
        counter = AllosUserCounters.objects.get(user_id_id=user.id)
        allowed = alloAllowed(selected_allo.allo_type, counter)
        return render(request, 'allos/alloRegistration.html', {'user': user, 'allo': selected_allo, 'allowed': allowed})
    else:
        messages.error(request, "Vous devez être connecté")


def alloAllowed(allo_type, counter):
    if allo_type == "A":
        return counter.biere
    elif allo_type == "B":
        return counter.gouter
    elif allo_type == "C":
        return counter.ptitdej
    elif allo_type == "D":
        return counter.menage
    elif allo_type == "E":
        return counter.car_wash
    elif allo_type == "F":
        return counter.klax
    elif allo_type == "G":
        return counter.cuisine
    elif allo_type == "H":
        return counter.courses
    else:
        return 0


def alloRequested(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        all_request = AllosRegistration.objects.filter(made=False)
        done_allos = AllosRegistration.objects.filter(made=True)

        return render(request, 'allos/alloRequested.html', {'user': user, 'allos': all_request, 'doneAllos': done_allos})
    else:
        messages.error(request, "Vous devez être connecté")


def takeOverAllo(request, id_take_allo):
    try:
        allo = AllosRegistration.objects.get(pk=id_take_allo)
    except AllosRegistration.DoesNotExist:
        allo = None
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if allo is not None and user is not None:
        allo.take_over = True
        allo.staff_id = request.user.id
        allo.save()

        return redirect('alloRequested')
    else:
        messages.error(request, "Erreur lors du chargement")


def dontTakeOverAllo(request, id_dontTake_allo):
    try:
        allo = AllosRegistration.objects.get(pk=id_dontTake_allo)
    except AllosRegistration.DoesNotExist:
        allo = None
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if allo is not None and user is not None:
        allo.take_over = False
        allo.staff_id = 0
        allo.save()

        return redirect('alloRequested')
    else:
        messages.error(request, "Erreur lors du chargement")


def staff(request):
    return render(request, 'staff.html')


def goals(request):
    try:
        registered = User.objects.filter(is_staff=False, is_superuser=False).count()
    except User.DoesNotExist:
        registered = 0

    return render(request, 'nav_links/goals.html', {'registered': registered})


def partners(request):
    return render(request, 'footers/partners.html')


def ourThanks(request):
    return render(request, 'footers/thanks.html')


def promises(request):
    return render(request, 'footers/campaignPromises.html')


def ourValues(request):
    return render(request, 'footers/ourValues.html')
