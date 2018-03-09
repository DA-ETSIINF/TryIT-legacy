from django.contrib import admin

from tickets.models import Validator
from volunteers.models import Schedule, Volunteer, VolunteerSchedule, VolunteerRole


class VolunteersAdmin(admin.ModelAdmin):
    
    list_display = ["name", "surname",  "get_rolelist", "android_phone", "phone", "active" ]
    list_display_links = ["name"]
    list_editable = ["active"]
    search_fields = ["name", "surname"]
    list_filter = ["rolelist"]
    actions = ['convert_to_validator', 'convert_to_assistant', 'mail_to_validator', 'mail_to_assistant', 'mail_schedule']

    # this function will hide volunteers role avoiding people to manually edit them
    def get_form(self, request, obj=None, **kwargs):
        if obj.rolelist:
            self.exclude = ("rolelist",)
        form = super(VolunteersAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_rolelist(self, obj):
        return "\n".join([ select.role for select in obj.rolelist.all()])
          
    def convert_to_validator(self, request, queryset):
        for obj in queryset:
            try:
                # is validator?
                obj.rolelist.get(role='validator')
            except:
                # convert to validator
                obj.rolelist.add(VolunteerRole.objects.get(role='validator'))
                Validator.objects.create(
                    name= obj.name,
                    volunteer = obj
                )
            else:
                #remove validator
                Validator.objects.get(volunteer=obj).delete()
                volunteer = obj.rolelist
                volunteer.remove(VolunteerRole.objects.get(role="validator"))


    convert_to_validator.short_description = "Convert to/delete validator"

    def convert_to_assistant(self, request, queryset):
        for obj in queryset:
            try:
                obj.rolelist.get(role='assistant')
            except:
                obj.rolelist.add(VolunteerRole.objects.get(role='assistant'))
            else:
                volunteer = obj.rolelist
                volunteer.remove(VolunteerRole.objects.get(role="assistant"))


    convert_to_assistant.short_description = "Convert to/delete assistant"

    def mail_to_validator(self, request, queryset):
        for obj in queryset:
                pass

    mail_to_validator.short_description = "Send mail to validator"

    def mail_to_assistant(self, request, queryset):
        for obj in queryset:
          pass

    mail_to_assistant.short_description = "Send mail to assistant"

    def mail_schedule(self, request, queryset):
        for obj in queryset:
            pass

    mail_schedule.short_description = "Send mail with schedule"


admin.site.register(Schedule)
admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(VolunteerSchedule)
admin.site.register(VolunteerRole)
