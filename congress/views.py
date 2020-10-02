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
from TryIT.settings_secret import PRIZE_PASSWORD
from congress.models import Streaming
from congress.serializers import StreamingSerializer
from editions.models import Edition, Session, Prize
from tickets.models import CheckIn, Ticket, Attendant


year_first_edition = 2013
tickets_first_year = 2016


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

