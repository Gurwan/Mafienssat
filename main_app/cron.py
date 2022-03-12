from datetime import datetime

from main_app.models import Allos, Event, Bets, StoreBets
from main_app.views import ratingRecalculation


def my_cron_bets():
    bets = Bets.objects.all()
    if bets is not None:
        for bet in bets:
            if bet.ended == datetime.now().strftime('%H:%M:%S'):
                bet.closed_bet = True
                bet.save()

                ratingRecalculation(bet.id)
                try:
                    made_bets = StoreBets.objects.filter(pk=bet.id)
                except StoreBets.DoesNotExist:
                    made_bets = None

                if made_bets is not None:
                    for b in made_bets:
                        b.blocked_bet = True
                        if b.RESULT == 'W':
                            b.bet_rate = bet.win_rate
                        else:
                            b.bet_rate = bet.lose_rate

                        b.save()


def my_cron_allos():
    all_allos = Allos.objects.all()
    if all_allos is not None:
        for allo in all_allos:
            if allo.end_date == datetime.now().strftime('%H:%M:%S'):
                allo.closed_allo = True
                allo.save()


def my_cron_events():
    events = Event.objects.all()
    if events is not None:
        for evt in events:
            if evt.event_date == datetime.now().strftime('%H:%M:%S'):
                evt.closed_event = True
                evt.save()