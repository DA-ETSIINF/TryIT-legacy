from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from events.models import Event, EventSession
from tickets.models import Attendant


class AddAttendantToSession(ModelSerializer):


    class Meta:
        model = Attendant
        fields = ('identity',)


class EventSessionSerializer(ModelSerializer):
    available = serializers.SerializerMethodField()

    def get_available(self, obj):
        return str(obj.capacity - obj.attendants.count())

    class Meta:
        model = EventSession
        fields = ("id", "date", "available")


class EventSerializer(ModelSerializer):

    sessions = serializers.SerializerMethodField()

    def get_sessions(self, obj):
        sessions = EventSessionSerializer(EventSession.objects.filter(event=obj).order_by('date'),
                                          read_only=True, many=True)
        return sessions.data

    class Meta:
        model = Event
        fields = ('id', 'name', 'sessions')

