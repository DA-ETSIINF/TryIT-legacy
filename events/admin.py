from django.contrib import admin

# Register your models here.
from events.models import Event, EventSession


class EventSessionAdmin(admin.ModelAdmin):
    list_display = ["event", "year", "date", "capacity", "assistants"]

    def year(self, obj):
        return obj.event.edition.year

    def assistants(self, obj):
        return obj.attendants.count()


admin.site.register(Event)
admin.site.register(EventSession, EventSessionAdmin)