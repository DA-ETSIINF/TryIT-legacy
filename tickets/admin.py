from django.contrib import admin

from tickets.models import TicketType, Ticket, CheckIn, Validator, Attendant

admin.site.register(TicketType)
admin.site.register(Ticket)
admin.site.register(CheckIn)
admin.site.register(Validator)
admin.site.register(Attendant)
