from django.contrib import admin

from tickets.models import Validator, Attendant
from volunteers.models import VolunteerSchedule, VolunteerRole



admin.site.register(VolunteerSchedule)
admin.site.register(VolunteerRole)
