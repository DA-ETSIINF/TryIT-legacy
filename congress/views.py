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
import datetime
import requests

from TryIT.settings_global import EDITION_YEAR
from TryIT.settings_secret import PRIZE_PASSWORD
from congress.models import Streaming
from congress.models import AttendanceSlot, Attendance
from congress.serializers import StreamingSerializer
from editions.models import Edition, Session, Prize
from tickets.models import CheckIn, Ticket, Attendant
from rest_framework.generics import UpdateAPIView

import json
from TryIT.settings_secret import BLOCKCHAIN_BACKEND


from TryIT.url_helper import create_context

year_first_edition = 2013
tickets_first_year = 2016


def home(request):
    edition = Edition.objects.get(year=EDITION_YEAR)
    if settings.LANDING:
        http_response = render(request, template_name='congress/landing.html', context=create_context({
            'edition': edition
        }))
    else:
        http_response = render(request, template_name='congress/home.html', context=create_context({
            'edition': edition
        }))
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
            res = StreamingSerializer(stream[0]).data # It suppose to exist one and only one stream...
            return Response({"title": res["title"], "url": res["url"], "streaming": True})
        return Response({"streaming": False})

class AttendanceApi(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StreamingSerializer
    interval = datetime.timedelta(0, 5 * 60) # 5 minutes

    def get_current_session(self):
        current_time = datetime.datetime.now()
        entries = AttendanceSlot.objects.all()
        current_intervals = list(filter(lambda x: (x.start_date < current_time and x.end_date > current_time), entries))
        return current_intervals

    def get(self, request): 
        current_intervals = self.get_current_session()
        if  len(current_intervals) > 0: 
            return Response({
                "attendance_slot_id": current_intervals[0].id,
                "start_date": current_intervals[0].start_date,
                "talk": current_intervals[0].session.title
                })
        else:
            return Response({"attendance_slot_id": None, "talk": None })
    
    def post(self, request):
        student_id = request.data["this_is_not_automated"]
        current_intervals = self.get_current_session()
        
        attendant_query = Attendant.objects.filter(edition__year=EDITION_YEAR,student_id=student_id)
        if student_id == None or current_intervals == None or len(current_intervals) == 0 or len(attendant_query) == 0:
            error = {'message': 'Algo ha ido mal'}
            return HttpResponseBadRequest(json.dumps(error))
        slot = current_intervals[0]
        attendant = attendant_query.first()
        attendance = Attendance(attendant=attendant, slot=slot)
        attendance.save()
        
        object_to_blockchain = { "user_hash": attendant.hash(), "slot_id": slot.id, "created_at": attendance.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"), "session_title": slot.session.title }
        ret = requests.post(BLOCKCHAIN_BACKEND, json=object_to_blockchain)
        return Response({"status": "OK" })


def AttendanceView(request):
    template_name = 'congress/asistencia.html'
    return render(request, template_name,context=create_context())


def workshops(request):
    edition = Edition.objects.get(year=EDITION_YEAR)
    workshops = Session.objects.filter(edition__year=EDITION_YEAR).filter(format__name='Taller')

    counter = 0  # I don't know how to get index of an element of an arraypa
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
    ed_2019 = Edition.objects.get(year='2019')
    ed_2019_dates = ed_2019.sessions.datetimes(field_name='start_date', kind='day')
    sessions_2019 = Session.objects.filter(edition__year='2019') \
        .filter(Q(format__name='Taller') | Q(format__name='Ponencia'))

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
        'sessions_2019': sessions_2019,
        'sessions_2017': sessions_2017,
        'ed_2016': ed_2016,
        'ed_2015': ed_2015,
        'ed_2014': ed_2014,
        'ed_2013': ed_2013,
        'ed_2019': ed_2019,
        'ed_2019_dates': ed_2019_dates,
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

        if data['token'] == PRIZE_PASSWORD:
            attendants = []

            id = data['sessionId']
            checkins = CheckIn.objects.filter(session__id=id)

            winner_list = list(map(lambda p: p.winner,
                                   Prize.objects.filter(winner__isnull=False, session__edition__year=EDITION_YEAR)))
            volunteer_list_email = list(map(lambda v: v.email, Attendant.objects.filter(active=True,
                                                edition__year=EDITION_YEAR).distinct()))
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
        .filter(student=True).filter(is_upm_student=True)

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
