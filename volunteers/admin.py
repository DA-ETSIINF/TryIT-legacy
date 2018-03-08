from django.contrib import admin

from tickets.models import Validator
from volunteers.models import Schedule, Volunteer, VolunteerSchedule, VolunteerRole


class ValidatorInLine(admin.StackedInline):
    model = Validator

class VolunteersAdmin(admin.ModelAdmin):
    list_display = ["name", "surname",  "expedient" ]
    list_display_links = ["name", "surname"]
    search_fields = ["name", "surname"]
    #list_editable = ["validator"]
    #actions = ['convert_to_validator']
    inlines = [ValidatorInLine]
    def response_action(self, request, queryset):
        self.queryset = Volunteer.objects.get()
    '''
    def convert_to_validator(self, request, queryset):

        print(Volunteer.objects.all)

    convert_to_validator.short_description = "Give selected volunteers the ability to check tickets (not working)"
    '''




admin.site.register(Schedule)
admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(VolunteerSchedule)
admin.site.register(VolunteerRole)