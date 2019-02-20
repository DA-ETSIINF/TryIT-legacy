
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response


from TryIT.settings_global import EDITION_YEAR

from events.models import Event, EventSession
from events.serializers import EventSerializer, AddAttendantToSession
from tickets.models import Attendant
from TryIT.url_helper import create_context




class EscapeRoomSessionsView(ListAPIView):
    queryset = Event.objects.all().filter(type__id=1, edition__year=EDITION_YEAR) # 0 is the Escape room type
    serializer_class = EventSerializer


class EscapeRoomAddAttendant(UpdateAPIView):
    queryset = EventSession.objects.all()
    serializer_class = AddAttendantToSession

    def post(self, request, *args, **kwargs):
        sessionevent = EventSession.objects.filter(id=self.kwargs['pk'])
        attendant = Attendant.objects.filter(identity=self.request.data['identity'], edition__year=EDITION_YEAR)
        # A filter will always return an list, if exists the event and/or the attendant,
        # the list must have only an element
        if sessionevent.count != 0 \
                and attendant.count != 0 \
                and sessionevent.filter(attendants=attendant[0]).count() == 0:
            sessionevent[0].attendants.add(attendant[0])
            sessionevent[0].save()
            return Response({"status": "Añadido correctamente! Te esperamos"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "No pudimos añadirte. Recuerda, debes tener la entrada y "
                                       "no haberte apuntado previamente a esta sesión"},
                            status=status.HTTP_400_BAD_REQUEST)


def EscapeRoomIndexView(request):
    template_name = 'events/escape-room.html'
    return render(request, template_name,context=create_context())
