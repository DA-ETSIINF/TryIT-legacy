from django.contrib import admin

from tickets.models import TicketType, Ticket, CheckIn, Validator, Attendant, Degree, School
from volunteers.models import VolunteerRole


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('edition', 'name', 'description',
                    'start_date', 'end_date',
                    'available_amount', 'price'
                    )


class CheckinAdmin(admin.ModelAdmin):
    list_display = ('attendant', 'session', 'validator', 'time_stamp')
    list_filter = ('session__edition__year',)
    search_fields = ('attendant__name', 'attendant__lastname')


class TicketAdmin(admin.ModelAdmin):
    list_filter = ('type__edition__year',)
    search_fields = ('id', 'attendant__name')


class ValidatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'volunteer')


class AttendantAdmin(admin.ModelAdmin):
    list_display = ('edition', 'name', 'lastname', 'email', 'phone',
                    'is_student', 'is_student_upm',
                    'college', 'degree', 'grade', 'identity',
                    "get_rolelist", "android_phone",
                    "phone", "active"
                    )
    # list_filter = ('college', 'degree', 'grade', 'student', 'upm_student')
    list_filter = ("rolelist", "registered_as_volunteer", "active",
                   'edition', 'is_student', 'is_upm_student', 'college',
                   'degree', 'grade',
                   )
    list_display_links = ["name"]
    list_editable = ["active"]
    search_fields = ('name', 'lastname', 'email', 'phone', 'identity', )
    actions = ['convert_to_validator', 'convert_to_assistant']


    def is_student(self, obj):
        return obj.student
    is_student.boolean = True

    def is_student_upm(self, obj):
        return obj.upm_student
    is_student_upm.boolean = True

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
                    Validator.objects.create(
                        name=obj.name,
                        volunteer=obj
                    )
                    obj.rolelist.add(VolunteerRole.objects.get(role='validator'))

                else:
                    # NOT remove validator, only remove reference (If remove db breaks so DONT)
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


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


class DegreeAdmin(admin.ModelAdmin):
    list_display = ('code', 'degree', 'school')


admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CheckIn, CheckinAdmin)
admin.site.register(Validator, ValidatorAdmin)
admin.site.register(Attendant, AttendantAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Degree, DegreeAdmin)
