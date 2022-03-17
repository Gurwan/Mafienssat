import os

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from decimal import *
from datetime import datetime

from django.template.loader import render_to_string
from django.templatetags import static
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from bet_klax import settings
from bet_klax.settings import EMAIL_HOST_USER, STATICFILES_DIRS
from .models import User, Bets, StoreBets, Event, EventsRegistration, AllosRegistration, Allos
from .forms import UserForm, AddBetForm, AddEventForm, AlloAdminForm
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str


def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.activate:
                login(request, user)

                return redirect('home')
            else:
                messages.error(request, "Vous devez activer votre compte, vérifier votre adresse enssat")
        else:
            messages.error(request, 'L\'utilisateur n\'existe pas ou tu t\'es trompé de mot de passe')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)

    return redirect('home')


def registerUser(request):
    if request.method != 'POST':
        form = UserForm()
        return render(request, 'register.html', {'form': form})
    else:
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            if user.email.split("@")[1] == "enssat.fr":
                user.save()

                current_site = get_current_site(request)
                subject = 'Activate Your Mafienssat Account'

                message = render_to_string('accountActivationEmail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })

                user_email = user.email
                send_mail(subject, message, EMAIL_HOST_USER, [user_email])

                return HttpResponse('<h2 style="color:rgb(165, 1, 1);">Please confirm your email address to complete the registration. After that go back to the website to login!</h2>')
            else:
                messages.error(request, "Vous devez utiliser votre adresse mail enssat")

        return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.activate = True
        user.save()

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def home(request):
    players = User.objects.all()
    try:
        last_events = Event.objects.filter(visible=True, closed_event=False).last()
    except Event.DoesNotExist:
        last_events = None

    return render(request, 'home.html', {'players': players, 'event': last_events})


def homeBetKlax(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    return render(request, 'bets/homeBets.html', {'user': user})


def betKlax(request):
    try:
        bets_done = StoreBets.objects.filter(user_id_id=request.user.id, closed_bet=False)
        bet = []
        for b in bets_done:
            bet.append(b.bet_id_id)
        bets = Bets.objects.exclude(id__in=bet).order_by("-id")

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
                messages.error(request, 'Erreur lors de la création du pari')

        bets = Bets.objects.all()

        return render(request, 'bets/betCreator.html', {'user': user, 'betform': betform, 'bets': bets})
    except User.DoesNotExist:
        messages.error(request, "Tu dois être membre du staff pour accéder à cette page")


def setVisibleBet(request, id_bet):
    try:
        bet = Bets.objects.get(pk=id_bet)
    except Bets.DoesNotExist:
        bet = None

    if bet is not None:
        bet.visible = True
        bet.save()

        return redirect('betCreator')

    else:
        messages.error(request, "Erreur lors de l'envoi de la requête")


def ratingRecalculation(id_bet):
    try:
        bet = Bets.objects.get(pk=id_bet)
    except Bets.DoesNotExist:
        bet = None

    if bet is not None:
        w_gains = float(bet.win_gains) + float(1)
        l_gains = float(bet.lose_gains) + float(1)

        w_rate = (w_gains + l_gains) / w_gains
        if w_rate > 50:
            w_rate = 50

        l_rate = (w_gains + l_gains) / l_gains
        if l_rate > 50:
            l_rate = 50

        bet.win_rate = Decimal(w_rate)
        bet.lose_rate = Decimal(l_rate)
        bet.save()


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

                return redirect("myBets")
            else:
                messages.error(request, "Tu n\'as pas assez de KlaxCoins espèce de rat")
        else:
            messages.error(request, "Tu as déja parié sur ce pari")
    else:
        messages.error(request, "Erreur lors de l'envoie dela requête")


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

                return redirect("myBets")
            else:
                messages.error(request, "Tu n\'as pas assez de KlaxCoins espèce de rat")
        else:
            messages.error(request, "Tu as déja parié sur ce pari")
    else:
        messages.error(request, "Erreur lors de l'envoi de la requête")


def myBets(request):
    try:
        finalizedBets = StoreBets.objects.filter(user_id_id=request.user.id, blocked_bet=True, closed_bet=False)
    except User.DoesNotExist:
        finalizedBets = None

    try:
        mybets = StoreBets.objects.filter(user_id_id=request.user.id, blocked_bet=False, closed_bet=False)
    except StoreBets.DoesNotExist:
        mybets = None

    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    try:
        myEndedBets = StoreBets.objects.filter(user_id_id=request.user.id, blocked_bet=True, closed_bet=True)
    except StoreBets.DoesNotExist:
        myEndedBets = None

    if user is not None:
        return render(request, 'bets/myBetKlax.html',
                      {'mybets': mybets, 'finalizedBets': finalizedBets, 'user': user, 'myEndedBets': myEndedBets})


def addGains(request, id_bet, gains):
    try:
        current_user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        current_user = None

    try:
        bet = StoreBets.objects.get(user_id_id=request.user.id, bet_id_id=id_bet, closed_bet=False, blocked_bet=False)
    except StoreBets.DoesNotExist:
        bet = None

    if current_user is not None and bet is not None:
        try:
            this_bet = Bets.objects.get(pk=bet.bet_id_id)
        except Bets.DoesNotExist:
            this_bet = None

        if current_user.klax_coins >= Decimal(abs(gains)) and this_bet is not None:
            if bet.gains + Decimal(abs(gains)) > 9999999999.99:
                bet.gains = Decimal(9999999999.99)
            else:
                bet.gains += Decimal(abs(gains))
            bet.save()
            if bet.result == 'W':
                if this_bet.win_gains + Decimal(abs(gains)) > 9999999999.99:
                    this_bet.win_gains = Decimal(9999999999.99)
                else:
                    this_bet.win_gains += Decimal(abs(gains))
            elif bet.result == 'L':
                if this_bet.lose_gains + Decimal(abs(gains)) > 9999999999.99:
                    this_bet.lose_gains = Decimal(9999999999.99)
                else:
                    this_bet.lose_gains += Decimal(abs(gains))

            this_bet.save()

            current_user.klax_coins -= Decimal(abs(gains))
            current_user.save()

            ratingRecalculation(bet.bet_id_id)
            return redirect("myBets")

        else:
            messages.error(request, "Tu n'as pas assez de KlaxCoins espèce de rat")
            return redirect("myBets")
    else:
        messages.error(request, "Il faut être connecté pour accéder à cette page")
        return redirect("myBets")


def finalizeBet(request, id_bet):
    try:
        current_user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        current_user = None
    try:
        bet = StoreBets.objects.get(bet_id_id=id_bet, user_id_id=current_user.id)
    except StoreBets.DoesNotExist:
        bet = None

    if current_user is not None and bet is not None:

        if bet.result == 'W':
            bet.bet_rate = bet.bet_id.win_rate
        elif bet.result == 'L':
            bet.bet_rate = bet.bet_id.lose_rate
        else:
            messages.error(request, "Le résultat du pari est inconnu")

        bet.blocked_bet = True
        bet.save()

        ratingRecalculation(bet.bet_id_id)

        return redirect("myBets")
    else:
        messages.error(request, "Tu dois être connecté pour accéder à cette page")


def setVisibleEvent(request, id_event):
    try:
        this_event = Event.objects.get(pk=id_event)
    except Event.DoesNotExist:
        this_event = None

    if this_event is not None:
        this_event.visible = True
        this_event.save()

        return redirect('eventCreator')

    else:
        messages.error(request, "Erreur lors de l'envoi de la requête")


def suBets(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:

        bets = Bets.objects.all()
        return render(request, "bets/suBets.html", {"user": user, "bets": bets})
    else:
        messages.error(request, "Vous devez être connecté")


def closeBet(request, id_bet):
    try:
        bets = StoreBets.objects.filter(bet_id_id=id_bet)
    except StoreBets.DoesNotExist:
        bets = None

    try:
        bet = Bets.objects.get(pk=id_bet)
    except Bets.DoesNotExist:
        bet = None

    if bet is not None and bets is not None:
        bet.closed_bet = True
        bet.save()

        for b in bets:
            b.blocked_bet = True
            b.closed_bet = True
            if b.RESULT == 'W':
                b.bet_rate = bet.win_rate
            else:
                b.bet_rate = bet.lose_rate

            b.closed_bet = True
            b.save()

        return redirect("suBets")

    else:
        messages.error(request, "Aucun pari enregistré")


def sendBetsKalxcoins(request, id_bet, result_bet):
    try:
        bets = StoreBets.objects.filter(bet_id_id=id_bet)
    except StoreBets.DoesNotExist:
        bets = None
    try:
        bet = Bets.objects.get(pk=id_bet)
    except Bets.DoesNotExist:
        bet = None

    if bet is not None:
        if bets is not None:

            for b in bets:
                if result_bet == "W" and b.result == 'W':
                    b.user_id.klax_coins += bet.win_rate * b.gains
                    b.final_result = 'W'
                elif result_bet == "L" and b.result == 'L':
                    b.user_id.klax_coins += bet.lose_rate * b.gains
                    b.final_result = 'W'
                else:
                    b.final_result = 'L'

                b.user_id.save()
                b.save()

            bet.result = result_bet
            bet.save()

            return redirect("suBets")

        else:
            bet.delete()

            return redirect("suBets")
    else:
        messages.error(request, "Aucun pari enregistré")


def deleteBet(request, id_bet):
    try:
        bet = Bets.objects.get(pk=id_bet)
    except Bets.DoesNotExist:
        bet = None

    if bet is not None:
        bet.delete()
    else:
        messages.error(request, "Ce bet n'existe pas")

    return redirect("suBets")


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
        registered_event = EventsRegistration.objects.filter(user_id_id=request.user.id)
    except EventsRegistration.DoesNotExist:
        registered_event = None

    if registered_event is not None:
        reg_event_id = []
        for e in registered_event:
            reg_event_id.append(e.event_id.id)
        if reg_event_id:
            events = Event.objects.exclude(id__in=reg_event_id)
            registered_event = Event.objects.filter(id__in=reg_event_id)
    else:
        messages.error(request, "Erreur lors de l'envoie de la requête")

    return render(request, 'events/event.html', {'events': events, 'user': user, 'registered': registered_event})


def readFileForHTML(file_name):
    all_lines = open(file_name).read().splitlines()
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
        this_event = Event.objects.get(pk=id_event)
    except Event.DoesNotExist:
        this_event = None

    if this_event is not None:

        infos = readFileForHTML('/var/www/bet_klax/static/events/' + this_event.event_name + '.txt')

        return render(request, 'events/eventPresentation.html', {'event': this_event, 'infos': infos})
    else:
        messages.error(request, "Erreur lors de l'envoie de la requête")

    return redirect("event")


def eventRegistration(request, event_id):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    try:
        done = EventsRegistration.objects.get(user_id_id=user.id, event_id_id=event_id)
    except EventsRegistration.DoesNotExist:
        done = None

    try:
        this_event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        this_event = None

    if done is None and user is not None and this_event is not None:

        if this_event.max_attendees != 0 and this_event.attendees_number < this_event.max_attendees:
            this_event.attendees_number += 1
            this_event.save()

            reg = EventsRegistration()
            reg.event_id = this_event
            reg.user_id = user
            reg.save()

            return redirect('event')
        else:
            messages.error(request, "Cet évènement est déja complet")
    else:
        messages.error(request, "Erreur lors de l'envoi de la requête")


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

            done = EventsRegistration.objects.get(user_id_id=request.user.id, event_id_id=event_id)
            done.delete()

            return redirect('event')
        else:
            messages.error(request, "Erreur lors de l'identification de l'évènement")
    else:
        messages.error(request,
                       "Un problème est survenu lors de votre inscription, veuillez réessayer et si cela persiste, contacter un admin")


def suEvents(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:

        events = Event.objects.all()
        return render(request, "events/suEvents.html", {"user": user, "events": events})
    else:
        messages.error(request, "Vous devez être connecté")


def closeEvent(request, id_event):
    try:
        this_event = Event.objects.get(pk=id_event)
    except Event.DoesNotExist:
        this_event = None

    if this_event is not None:
        this_event.closed_event = True
        this_event.save()

        return redirect("suEvents")
    else:
        messages.error(request, "Erreur lors de l'envoie dela requête")


def deleteEvent(request, id_event):
    try:
        evt = Event.objects.get(pk=id_event)
    except Event.DoesNotExist:
        evt = None

    if evt is not None:
        evt.delete()
    else:
        messages.error(request, "Cet event n'existe pas")

    return redirect("suEvents")


def liste(request):
    return render(request, 'nav_links/liste.html')


def klaxment(request):
    userList = User.objects.filter(is_staff=False, is_superuser=False, from_list=False, activate=True).order_by('-klax_coins')
    data = {'userList': userList}

    return render(request, 'nav_links/klaxment.html', data)


def homeAllos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    return render(request, 'allos/homeAllos.html', {'user': user})


def allos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        try:
            registered_allo = AllosRegistration.objects.filter(user_id=user)
        except AllosRegistration.DoesNotExist:
            registered_allo = None

        if registered_allo is not None:
            ids = []
            for a in registered_allo:
                ids.append(a.allo_id.id)

            unregistered_allos = Allos.objects.exclude(id__in=ids)

        else:
            unregistered_allos = Allos.objects.all()
    else:
        unregistered_allos = Allos.objects.all()

    return render(request, 'allos/allos.html', {'user': user, 'allos': unregistered_allos})


def myAllos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        my_allos = AllosRegistration.objects.filter(user_id_id=user.id)

        all_allos = Allos.objects.filter(visible=True)
        types = []
        for allo in all_allos:
            types.append(allo.allo_type)

        return render(request, 'allos/myAllos.html',
                      {'user': user, 'allos': my_allos, 'allos_types': types})
    else:
        messages.error(request, "Vous devez être connecté")


def sendAllo(request, date, time, allo_id):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None and date is not None and time is not None and allo_id is not None:
        date_time = date + " " + time + ":00"
        try:
            selected_allo = Allos.objects.get(id=allo_id)
        except Allos.DoesNotExist:
            selected_allo = None

        if selected_allo is not None:
            allo = AllosRegistration()
            allo.user_id = user
            allo.allo_id = selected_allo
            allo.date = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S')
            allo.save()

        return redirect('myAllos')

    else:
        messages.error(request, "Utilisateur non trouvé")


def removeAllo(request, id_allo):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:

        try:
            allo = AllosRegistration.objects.get(pk=id_allo, user_id_id=user.id)
        except AllosRegistration.DoesNotExist:
            allo = None

        if allo is not None:

            allo.delete()

            return redirect('myAllos')
        else:
            messages.error(request, "Erreur lors de l'envoie de la requête")
    else:
        messages.error(request, "Vous devez être connecté")


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


def setVisibleAllo(request, id_allo):
    try:
        allo = Allos.objects.get(pk=id_allo)
    except Allos.DoesNotExist:
        allo = None

    if allo is not None:
        allo.visible = True
        allo.save()

        return redirect('alloCreator')

    else:
        messages.error(request, "Erreur lors de l'envoi de la requête")


def alloRegistration(request, id_allo):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None
    try:
        selected_allo = Allos.objects.get(pk=id_allo)
    except Allos.DoesNotExist:
        selected_allo = None

    if user is not None and selected_allo is not None:
        return render(request, 'allos/alloRegistration.html', {'user': user, 'allo': selected_allo})
    else:
        messages.error(request, "Vous devez être connecté")


def alloRequested(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        all_request = AllosRegistration.objects.filter(made=False)
        done_allos = AllosRegistration.objects.filter(made=True)

        return render(request, 'allos/alloRequested.html',
                      {'user': user, 'allos': all_request, 'doneAllos': done_allos})
    else:
        messages.error(request, "Vous devez être connecté")


def finalizeAllo(request, id_finalized_allo):
    try:
        allo = AllosRegistration.objects.get(pk=id_finalized_allo)
    except AllosRegistration.DoesNotExist:
        allo = None
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if allo is not None and user is not None:
        allo.made = True
        allo.staff_id = request.user.id
        allo.save()

        return redirect('alloRequested')
    else:
        messages.error(request, "Erreur lors du chargement")


def suAllos(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:

        all_allos = Allos.objects.all()
        return render(request, "allos/suAllos.html", {"user": user, "allos": all_allos})
    else:
        messages.error(request, "Vous devez être connecté")


def closeAllo(requets, id_allo):
    try:
        allo = Allos.objects.get(pk=id_allo)
    except Allos.DoesNotExist:
        allo = None

    if allo is not None:
        allo.closed_allo = True
        allo.save()

        return redirect("suAllos")
    else:
        messages.error(requets, "Erreur lors de l'envoie de la requête")


def alloEmailConfirmation(request, id_allo):
    try:
        allo = AllosRegistration.objects.get(pk=id_allo)
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

        return render(request, "allos/alloEmailForm.html", {'user': user, 'allo': allo})
    else:
        messages.error(request, "Erreur lors du chargement de la page")


def sendAlloEmailConfirmation(request, date, time, allo_id):
    try:
        requested_allo = AllosRegistration.objects.get(pk=allo_id)
    except AllosRegistration.DoesNotExist:
        requested_allo = None

    if date is not None and time is not None and requested_allo is not None:
        try:
            staff_user = User.objects.get(pk=requested_allo.staff_id)
        except User.DoesNotExist:
            staff_user = None

        if staff_user is not None:
            date_time = date + " à " + time
            user_email = requested_allo.user_id.email
            subject = requested_allo.allo_id.get_allo_type_display()

            body = {
                'line1': 'Yo,',
                'line2': '',
                'line3': getAlloSentenceType(requested_allo.allo_id.allo_type, date_time),
                'line4': '',
                'line5': 'On va prendre contact avec toi incessamment sous peu.',
                'line6': 'Si tu n\'as pas reçu de message avant le jour de ta demande, tu peux contacter ' + staff_user.first_name + ' ' + staff_user.last_name + '.',
                'line7': '',
                'line8': 'La bise,',
                'line9': 'Mafienssat',
            }

            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, EMAIL_HOST_USER, [user_email], fail_silently=True)
            except BadHeaderError:
                messages.error(request, "Erreur lors de l'envoie de l'email")
                return redirect('alloEmailConfirmation')

            return redirect('alloRequested')

        else:
            messages.error(request, "staff non trouvé")
    else:
        messages.error(request, "La requête est vide, veuillez réessayer")


def getAlloSentenceType(allo_type, date):
    if allo_type == "A":
        return "Askip t'es en dèche de bière ? On se donne rdv le " + date + "."
    elif allo_type == "B":
        return "Alors on à une p'tite fringale ? Bouge pas on arrive le " + date + "."
    elif allo_type == "C":
        return "Tu as besoin que maman te prépare ton p'tit dej ? On peut la remplacer le " + date + "."
    elif allo_type == "D":
        return "On passera nettoyer ta merde le " + date + "."
    elif allo_type == "E":
        return "Les filles chaudes de ta région laveront ta caisse le " + date + "."
    elif allo_type == "F":
        return "Le klaxeur fou va prendre contact avec toi pour transmettre ta missive le " + date + "."
    elif allo_type == "G":
        return "On t'apporte le petit plat du chef le " + date + "."
    elif allo_type == "H":
        return "On s'occupe de t'apporter tes courses pour le " + date + "."
    else:
        return ""


def deleteAllo(request, id_allo):
    try:
        allo = Allos.objects.get(pk=id_allo)
    except Allos.DoesNotExist:
        allo = None

    if allo is not None:
        allo.delete()
    else:
        messages.error(request, "Ce allo n'existe pas")

    return redirect("suAllos")


def staff(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:

        return render(request, 'staff.html', {'user': user})
    else:
        messages.error(request, "Vous devez être staff")


def suUsers(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        user = None

    if user is not None:
        try:
            registered = User.objects.filter(from_list=False)
        except User.DoesNotExist:
            registered = None

        try:
            from_list = User.objects.filter(from_list=True, is_superuser=False, is_staff=False)
        except User.DoesNotExist:
            from_list = None

        try:
            staff_list = User.objects.filter(is_staff=True)
        except User.DoesNotExist:
            staff_list = None

        try:
            su_list = User.objects.filter(is_superuser=True)
        except User.DoesNotExist:
            su_list = None

        return render(request, "staffUsers.html", {"user": user, "registered": registered, "from_list": from_list, "staff_list": staff_list, "su_list": su_list})
    else:
        messages.error(request, "Vous devez être connecté")


def goals(request):
    try:
        registered = User.objects.filter(is_staff=False, is_superuser=False, from_list=False).count()
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
