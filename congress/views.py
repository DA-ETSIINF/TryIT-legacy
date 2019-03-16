import json
import random
import re

from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from TryIT.settings_global import EDITION_YEAR
from congress.models import Streaming
from congress.serializers import StreamingSerializer
from editions.models import Edition, Session, Prize
from tickets.models import CheckIn, Ticket, Attendant
#from volunteers.models import Volunteer

from TryIT.url_helper import create_context

year_first_edition = 2013
tickets_first_year = 2016


def home(request):
    if settings.LANDING:
        http_response = render(request, template_name='congress/landing.html', context=create_context())
    else:
        http_response = render(request, template_name='congress/home.html', context=create_context())
    return http_response


def activities(request):
    edition = Edition.objects.get(year=EDITION_YEAR)
    dates = edition.sessions.datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/activities.html', context=create_context({
        'edition': edition,
        'dates': dates
    }))


def contests(request):
    return render(request, template_name='congress/contests.html', context=create_context())


def streaming(request):
    return render(request, template_name='congress/streaming.html', context=create_context())


class streamingApi(GenericAPIView):
    queryset = Streaming.objects.all().filter(edition__year=EDITION_YEAR)
    serializer_class = StreamingSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        stream = Streaming.objects.all().filter(edition__year=EDITION_YEAR)
        if stream.exists():

            return Response(StreamingSerializer(stream[0]).data)

        return Response({"details": "Ups!! No hay video todavia"}, status=status.HTTP_404_NOT_FOUND)


def workshops(request):
    edition = Edition.objects.get(year=EDITION_YEAR)
    workshops = Session.objects.filter(edition__year=EDITION_YEAR).filter(format__name='Taller')

    counter = 0  # I don't know how to get index of an element of an array
    for workshop in workshops:
        description = workshop.description
        urls = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[\/.?&+!*=\-])+(?![^,!;:\s)])', description)  # Find urls
        for url in urls:
            href = "<a href=\"" + url + "\">" + url + "</a>"  # added ahref label(HTML)
            workshop.description = workshop.description.replace(url, href)
        counter += 1

    return render(request, template_name='congress/workshops.html', context=create_context({
        'edition': edition,
        'workshops': workshops
    }))


def contact(request):
    return render(request, template_name='congress/contact.html', context=create_context())


def last_editions(request):
    ed_2018 = Edition.objects.get(year='2018')
    ed_2018_dates = ed_2018.sessions.datetimes(field_name='start_date', kind='day')
    sessions_2018 = Session.objects.filter(edition__year='2018') \
        .filter(Q(format__name='Taller') | Q(format__name='Ponencia'))
    ed_2017 = Edition.objects.get(year='2017')
    ed_2017_dates = ed_2017.sessions.datetimes(field_name='start_date', kind='day')
    sessions_2017 = Session.objects.filter(edition__year='2017') \
        .filter(Q(format__name='Taller') | Q(format__name='Ponencia'))
    ed_2016 = Edition.objects.get(year='2016')
    ed_2016_dates = ed_2016.sessions.datetimes(field_name='start_date', kind='day')
    ed_2015 = Edition.objects.get(year='2015')
    ed_2015_dates = ed_2015.sessions.datetimes(field_name='start_date', kind='day')
    ed_2014 = Edition.objects.get(year='2014')
    ed_2014_dates = ed_2014.sessions.datetimes(field_name='start_date', kind='day')
    ed_2013 = Edition.objects.get(year='2013')
    ed_2013_dates = ed_2013.sessions.datetimes(field_name='start_date', kind='day')

    return render(request, template_name='congress/last_editions.html', context=create_context({
        'sessions_2018': sessions_2018,
        'sessions_2017': sessions_2017,
        'ed_2016': ed_2016,
        'ed_2015': ed_2015,
        'ed_2014': ed_2014,
        'ed_2013': ed_2013,
        'ed_2018_dates': ed_2018_dates,
        'ed_2017_dates': ed_2017_dates,
        'ed_2016_dates': ed_2016_dates,
        'ed_2015_dates': ed_2015_dates,
        'ed_2014_dates': ed_2014_dates,
        'ed_2013_dates': ed_2013_dates
    }))


def prizes(request):
    edition = Edition.objects.get(year=EDITION_YEAR)
    prizes = Prize.objects.all() \
        .filter(session__edition__year=EDITION_YEAR) \
        .filter(hide=False) \
        .order_by('session__start_date')

    return render(request, template_name='congress/prizes.html', context=create_context({
        'edition': edition,
        'prizes': prizes
    }))


@csrf_exempt
def get_winner(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        if data['token'] == 'pass':
            attendants = []

            id = data['sessionId']
            checkins = CheckIn.objects.filter(session__id=id)


            winner_list = list(map(lambda p: p.winner,
                                   Prize.objects.filter(winner__isnull=False, session__edition__year=EDITION_YEAR)))
            volunteer_list_email = list(map(lambda v: v.email, Volunteer.objects.filter(active=True,
                                                                                        volunteerschedule__schedule__edition__year=EDITION_YEAR).distinct()))
            # Skip last winners and volunteers
            for check in checkins:
                attendant = check.attendant
                if attendant not in winner_list and attendant.email not in volunteer_list_email:
                    attendants.append(attendant)

            if len(attendants) == 0:
                error = {'id': 3, 'message': 'No hay ckeckins'}
                return HttpResponseBadRequest(json.dumps(error))

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


def stats(request):
    numTickets = []
    numCheckIn = []

    for year_temp in range(tickets_first_year, EDITION_YEAR + 1):
        numTickets.append(Ticket.objects.filter(type__edition__year=year_temp).count())
        temp = CheckIn.objects.filter(session__edition__year=year_temp)
        unique = []
        for t in temp:
            if t.attendant_id not in unique:
                unique.append(t.attendant_id)
        numCheckIn.append(len(unique))

    # select s.id, s.title, count(s.id) from tickets_checkin c join editions_session s on c.session_id=s.id where s.edition_id=5 group by s.id
    checkIn = CheckIn.objects.filter(session__edition__year=EDITION_YEAR).values('session__title').annotate(
        count=Count('session_id')).order_by('session__start_date')

    checkInOrder = checkIn.order_by('count')
    checkInUnTop = checkInOrder[0:10]

    # checkInTop = sorted(checkIn, key=lambda checkin : checkin)
    checkInTop = checkInOrder[::-1][0:10]

    return render(request, template_name='congress/stats.html', context=create_context({
        'tickets': numTickets[::-1],
        'numCheckIn': numCheckIn[::-1],
        'checkInTop': checkInTop,
        'checkInUnTop': checkInUnTop,
        'checkIn': checkIn
    }))


def stats_charts(request):
    numTickets = Ticket.objects.filter(type__edition__year=EDITION_YEAR).count()
    checkin = CheckIn.objects.filter(session__edition__year=EDITION_YEAR)
    uniqueCheckin = []
    for check in checkin:
        if check.attendant_id not in uniqueCheckin:
            uniqueCheckin.append(check.attendant_id)
    numAttendants = len(uniqueCheckin)

    # Chart assistance
    chartAttendants = {'data': [numAttendants, numTickets - numAttendants],
                       'label': ['Asisten', 'No asisten'],
                       'backgroundColor': ["#FF6384", "#36A2EB"]}

    # Chart grade
    attendantsUpm = Attendant.objects.filter(id__in=uniqueCheckin) \
        .filter(student=True).filter(upm_student=True)

    numGrade = []
    for i in range(1, 5):
        numGrade.append(attendantsUpm.filter(grade=i).count())

    chartGrade = {'data': numGrade,
                  'label': ['1º', '2º', '3º', '4º'],
                  'backgroundColor': ["#FF6384", "#4BC0C0", "#FFCE56", "#36A2EB"]}

    data = {'chartAttendants': chartAttendants, 'chartGrade': chartGrade}
    return HttpResponse(json.dumps(data))


def hashcode(request):
    return render(request, template_name='congress/hashcode.html',context=create_context())
