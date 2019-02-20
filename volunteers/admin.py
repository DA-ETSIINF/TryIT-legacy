from django.contrib import admin

from tickets.models import Validator
from volunteers.models import Volunteer, VolunteerSchedule, VolunteerRole


class VolunteersAdmin(admin.ModelAdmin):    
    list_display = ["name", "lastname", "get_rolelist", "android_phone", "phone", "active"]
    list_display_links = ["name"]
    list_editable = ["active"]
    search_fields = ["name", "lastname"]
    list_filter = ["rolelist"]
    actions = ['convert_to_validator', 'convert_to_assistant']
  

    def name(self, obj):
        return obj.identity.name
    def lastname(self, obj):
        return obj.identity.lastname
    def phone(self, obj):
        return obj.identity.phone
    def get_rolelist(self, obj):
        return "\n".join([select.role for select in obj.rolelist.all()])

    def convert_to_validator(self, request, queryset):
        for obj in queryset:
            if obj.active:
                # is validator?
                if not obj.rolelist.filter(role='validator').exists():
                    # convert to validator
                    obj.rolelist.add(VolunteerRole.objects.get(role='validator'))
                    Validator.objects.create(
                        name=obj.identity.name,
                        volunteer=obj
                    )
                else:
                    # NOT remove validator, only remove reference
                    validator = Validator.objects.get(volunteer=obj)
                    validator.volunteer = None
                    validator.save()
                    volunteer = obj.rolelist
                    volunteer.remove(VolunteerRole.objects.get(role="validator"))

    convert_to_validator.short_description = "Convert to/delete validator"

    def convert_to_assistant(self, request, queryset):
        for obj in queryset:
            if obj.active:
                if not obj.rolelist.filter(role='assistant').exists():
                    obj.rolelist.add(VolunteerRole.objects.get(role='assistant'))
                else:
                    volunteer = obj.rolelist
                    volunteer.remove(VolunteerRole.objects.get(role="assistant"))

    convert_to_assistant.short_description = "Convert to/delete assistant"


admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(VolunteerSchedule)
admin.site.register(VolunteerRole)
