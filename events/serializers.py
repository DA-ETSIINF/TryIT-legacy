from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from events.models import Event, EventSession
from tickets.models import Attendant


class AddAttendantToSession(ModelSerializer):


    class Meta:
        model = Attendant
        fields = ('identity',)


class EventSessionSerializer(ModelSerializer):
    this_is_just_a_normal_var_that_represent_the_number_of_people_already_registered_made_with_love_by_dani_and_max \
        = serializers.SerializerMethodField()

    def get_this_is_just_a_normal_var_that_represent_the_number_of_people_already_registered_made_with_love_by_dani_and_max(self, obj):
        return obj.attendants.count()

    class Meta:
        model = EventSession
        fields = ("id", "date", "capacity",
                  "this_is_just_a_normal_var_that_represent_the_number_of_"
                  "people_already_registered_made_with_love_by_dani_and_max")


class EventSerializer(ModelSerializer):

    sessions = serializers.SerializerMethodField()

    def get_sessions(self, obj):
        sessions = EventSessionSerializer(EventSession.objects.filter(event=obj).order_by('date'),
                                          read_only=True, many=True)
        return sessions.data

    class Meta:
        model = Event
        fields = ('id', 'name', 'sessions')

