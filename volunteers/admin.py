from django.contrib import admin

from tickets.models import Validator
from volunteers.models import Schedule, Volunteer, VolunteerSchedule, VolunteerRole




class VolunteersAdmin(admin.ModelAdmin):
    
    list_display = ["name", "surname",  "expedient", "get_rolelist" ]
    list_display_links = ["name", "surname"]
    search_fields = ["name", "surname"]
    list_filter = ["rolelist"]
    actions = ['convert_to_validator']
  
    def response_action(self, request, queryset):
        self.queryset = Volunteer.objects.get()

        
    def get_rolelist(self, obj):
        return "\n".join([ select.role for select in obj.rolelist.all()])
          
    def convert_to_validator(self, request, queryset):
        for obj in queryset:
            Validator.objects.create(
                name= obj.name,
                volunteer = obj.pk
            )
        
    convert_to_validator.short_description = "Convert to validator"



admin.site.register(Schedule)
admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(VolunteerSchedule)
admin.site.register(VolunteerRole)
