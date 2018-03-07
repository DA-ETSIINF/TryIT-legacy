from django.contrib import admin



from volunteers.models import Schedule, Volunteer, VolunteerSchedule

class VolunteersAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "validator", "expedient"]
    list_display_links = ["name", "surname"]
    search_fields = ["name", "surname"]
    list_editable = ["validator"]
    actions = ['convert_to_validator']

    class Meta:
        model = Volunteer

    def convert_to_validator(self, request, queryset):
        queryset.update(status='p')

    convert_to_validator.short_description = "Give selected volunteers the ability to check tickets (not working)"

admin.site.register(Schedule)
admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(VolunteerSchedule)