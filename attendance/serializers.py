import json

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from TryIT.settings_global import EDITION_YEAR
from editions.models import Session, Track
from tickets.models import CheckIn, Attendant


class AttendanceSerializer(ModelSerializer):
    edition = serializers.SerializerMethodField()

    def get_edition(self, obj):
        return obj.attendant.edition.year

    talks = serializers.SerializerMethodField()

    def get_talks(self, obj):
        get_ticket = CheckIn.objects.filter(
            session__edition__year=obj.attendant.edition.year,
            attendant__identity=str(obj.attendant.identity))
        # print(get_ticket.select_for_update('session_title'))
        return get_ticket.all().select_for_update('session_title').all().values('session__title', 'session__start_date')

    ntalks = serializers.SerializerMethodField()

    def get_ntalks(self, obj):
        track = Track.objects.filter()[1] # get Principal track, determines talks accounted for ECTS
        sessions = Session.objects \
            .filter(edition__year=obj.attendant.edition.year) \
            .filter(track=track)
        return sessions.count()
    
    first_day_of_event = serializers.SerializerMethodField()
    def get_first_day_of_event(self, obj):
        return obj.attendant.edition.start_date

    # TODO when volunteers are linked to attendant, finish this
    #def is_volunteer(self, obj):
      #  return True if str(obj.attendant.identity) else False

    class Meta:
        model = CheckIn
        fields = ('edition',  'ntalks', 'talks', 'first_day_of_event')


class CheckInSerializer(ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'


class AttendantSerializer(ModelSerializer):
    class Meta:
        model = Attendant
        fields = '__all__'
