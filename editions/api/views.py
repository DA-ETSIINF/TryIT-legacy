from django.db.models import Q
from rest_framework import viewsets

from editions.api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EditionViewSet(viewsets.ModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class YearSessionsViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.filter(edition__year='2017') \
        .filter(Q(format__name='Taller') | Q(format__name='Ponencia'))
    serializer_class = YearSessionsSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
