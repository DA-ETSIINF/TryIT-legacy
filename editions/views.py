import json

from django.db.models import Count, Q
from rest_framework.generics import ListAPIView

from editions.api.serializers import EditionSerializer, SessionSerializer, OrganizerSerializer, SponsorsSerializer
from editions.models import Edition, Session, Organizer, CompanySponsorType
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render

from events.models import Event
from events.serializers import EventSerializer


@csrf_exempt
def get_editions(request):
    if request.method == 'GET':
        editions = Edition.objects.all()
        return HttpResponse(editions, content_type='application/json')
    else:
        return HttpResponseNotAllowed(permitted_methods='GET')


class GetAllEditions(ListAPIView):
    serializer_class = EditionSerializer
    queryset = Edition.objects.all()


class GetTalks(ListAPIView):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get_queryset(self):
        # I HATE HARDCODING
        return Session.objects.all().filter(edition__year=self.kwargs['year'], track__name="Principal" or "Extra",)


class GetWorkshops(ListAPIView):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get_queryset(self):
        # I HATE HARDCODING
        return Session.objects.all().filter(edition__year=self.kwargs['year'], track__name="Track",)


class GetEvents(ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        return Event.objects.all().filter(edition__year=self.kwargs['year'])


class GetOrganizers(ListAPIView):
    serializer_class = OrganizerSerializer
    queryset = Organizer.objects.all()

    def get_queryset(self):
        return Organizer.objects.all().filter(edition__year=self.kwargs['year'])


class GetSponsors(ListAPIView):
    serializer_class = SponsorsSerializer
    queryset = CompanySponsorType.objects.all()

    def get_queryset(self):
        bronce = Count('company',  filter=Q(sponsor_type__id=1))
        plata = Count('company',  filter=Q(sponsor_type__id=2))
        return CompanySponsorType.objects.all().filter(edition__year=self.kwargs['year'])


