from django.contrib import admin

from volunteers.models import VolunteerSchedule, VolunteerRole


admin.site.register(VolunteerSchedule)
admin.site.register(VolunteerRole)
