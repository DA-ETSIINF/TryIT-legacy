from django.db.models.functions import Lower
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from rest_framework.generics import ListAPIView

from TryIT.settings_global import EDITION_YEAR
from attendance.serializers import AttendanceSerializer
from editions.models import Session
from tickets.models import CheckIn, Attendant, Ticket


def AttendanceIndexView(request):
    template_name = 'attendance/attendance.html'
    return render(request, template_name=template_name)


class ListAttendanceECTs(ListAPIView):

    serializer_class = AttendanceSerializer

    def get_queryset(self):
        return Ticket.objects.all().filter(
            attendant__identity=str(self.kwargs['dni']),
            type__edition__year=self.kwargs['edition'])
