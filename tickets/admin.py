from django.contrib import admin

from tickets.models import TicketType, Ticket, CheckIn, Validator, Attendant, Degree, School

admin.site.register(TicketType)
admin.site.register(Ticket)
admin.site.register(CheckIn)
admin.site.register(Validator)
admin.site.register(Attendant)
admin.site.register(School)
admin.site.register(Degree)
