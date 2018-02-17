from django.contrib import admin

from volunteers.models import Schedule, Volunteer, VolunteerSchedule

admin.site.register(Schedule)
admin.site.register(Volunteer)
admin.site.register(VolunteerSchedule)
