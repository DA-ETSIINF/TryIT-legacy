from django.contrib import admin

from volunteers.models import RegisterVolunteers

admin.site.volunteers(RegisterVolunteers)
