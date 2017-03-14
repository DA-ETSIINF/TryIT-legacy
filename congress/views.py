import json
import random

from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from editions.models import Edition, Session, Prize
from register.models import RegisterCompany
from tickets.models import CheckIn, Ticket


def home(request):
    return render(request, template_name='congress/home.html')


def activities(request):
    edition = Edition.objects.get(year='2017')
    dates = edition.sessions.datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/activities.html', context={
        'edition': edition,
        'dates': dates
    })


def contests(request):
    return render(request, template_name='congress/contests.html')


def workshops(request):
    workshops = Session.objects.filter(edition__year='2017').filter(format__name='Taller')

    return render(request, template_name='congress/workshops.html', context={
        'workshops': workshops
    })


def contact(request):
    return render(request, template_name='congress/contact.html')


def last_editions(request):
    ed_2016 = Edition.objects.get(year='2016')
    ed_2016_dates = ed_2016.sessions.datetimes(field_name='start_date', kind='day')
    ed_2015 = Edition.objects.get(year='2015')
    ed_2015_dates = ed_2015.sessions.datetimes(field_name='start_date', kind='day')
    ed_2014 = Edition.objects.get(year='2014')
    ed_2014_dates = ed_2014.sessions.datetimes(field_name='start_date', kind='day')
    ed_2013 = Edition.objects.get(year='2013')
    ed_2013_dates = ed_2013.sessions.datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/last_editions.html', context={
        'ed_2016': ed_2016,
        'ed_2015': ed_2015,
        'ed_2014': ed_2014,
        'ed_2013': ed_2013,
        'ed_2016_dates': ed_2016_dates,
        'ed_2015_dates': ed_2015_dates,
        'ed_2014_dates': ed_2014_dates,
        'ed_2013_dates': ed_2013_dates
    })


def tickets(request):
    return render(request, template_name='congress/tickets.html')


def register(request):
    return render(request, template_name='congress/register.html', context={
        'sponsor_types': RegisterCompany.SPONSOR_TYPE,
        'dates': RegisterCompany.SPONSOR_DATE,
        'types': RegisterCompany.TYPE
    })


def contests_winners(request):
    prizes = Prize.objects.all().filter(hide=False).order_by('session__start_date')

    return render(request, template_name='congress/contests_winners.html', context={
        'prizes': prizes
    })


@csrf_exempt
def get_winner(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        if data['token'] == 'pass':
            attendants = []

            id = data['sessionId']
            checkins = CheckIn.objects.filter(session__id=id)
            for check in checkins:
                attendants.append(check.attendant)

            # Randomize
            winner = random.choice(attendants)
            winner_data = {'name': winner.name + ' ' + winner.lastname, 'id': winner.id}

            # Save winner
            prize = Prize.objects.get(id=data['prizeId'])
            prize.winner = winner
            prize.save()

            return HttpResponse(json.dumps(winner_data))

        else:
            error = {'id': 2, 'message': 'Error en la validación'}
            return HttpResponseBadRequest(json.dumps(error))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def stats (request):
    tickets = Ticket.objects.filter(type__edition__year="2017").count()
    # select s.id, s.title, count(s.id) from tickets_checkin c join editions_session s on c.session_id=s.id where s.edition_id=5 group by s.id
    checkIn = CheckIn.objects.filter(session__edition__year="2017").values('session__title').annotate(count=Count('session_id')).order_by('session__start_date')

    return render(request, template_name='congress/stats.html', context={
        'tickets': tickets,
        'checkIn': checkIn
    })