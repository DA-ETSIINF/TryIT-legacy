
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from TryIT.settings_global import EDITION_YEAR

from events.models import Event, EventSession
from events.serializers import EventSerializer, AddAttendantToSession
from tickets.models import Attendant
from TryIT.url_helper import create_context



class EscapeRoomSessionsView(ListAPIView):
    queryset = Event.objects.all().filter(type__id=1, edition__year=EDITION_YEAR) # 1 is the Escape room type
    serializer_class = EventSerializer


class EscapeRoomAddAttendant(UpdateAPIView):
    queryset = EventSession.objects.all()
    serializer_class = AddAttendantToSession
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        selectedsession = EventSession.objects.filter(id=self.kwargs['pk'])
        attendant = Attendant.objects.filter(identity=self.request.data['identity'].strip().upper(), edition__year=EDITION_YEAR)
        attendant_in_event = EventSession.objects.filter(event__id=selectedsession[0].event.id,
                                                         attendants__in=attendant).all().count()
        # A filter will always return an list, if exists the event and/or the attendant,
        # the list must have only an element

        #We first check if the session exists, then if there is availability and last if the attendant is not already
        # registered in a session
        if selectedsession.count() == 0:
            return Response({"message": "La sesión no existe"}, status=status.HTTP_404_NOT_FOUND)

        if selectedsession[0].attendants.count() + 1 >= selectedsession[0].capacity:
            return Response({"message": "La sesión esta llena"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if attendant_in_event != 0:
            return Response({"message": "Ya estas apuntado a una sesión"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        selectedsession[0].attendants.add(attendant[0])
        selectedsession[0].save()
        return Response({"message": "Añadido correctamente! Te esperamos"}, status=status.HTTP_201_CREATED)


def EscapeRoomIndexView(request):
    template_name = 'events/escape-room.html'
    return render(request, template_name,context=create_context())
