from django.contrib import admin

from tickets.models import TicketType, Ticket, CheckIn, Validator, Attendant, Degree, School


class CheckinAdmin(admin.ModelAdmin):
    list_display = ('attendant', 'session', 'validator', 'time_stamp')
    list_filter = ('session__edition__year',)
    search_fields = ('attendant__name', 'attendant__lastname')


class TicketAdmin(admin.ModelAdmin):
    list_filter = ('type__edition__year',)
    search_fields = ('id', 'attendant__name')


admin.site.register(TicketType)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CheckIn, CheckinAdmin)
admin.site.register(Validator)
admin.site.register(Attendant)
admin.site.register(School)
admin.site.register(Degree)
