from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin, ImportExportModelAdmin

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





class AttendantAdmin(ImportExportModelAdmin, admin.ModelAdmin,):

    import__fields = ('name', 'lastname')

    list_display = ('edition', 'name', 'lastname', 'email', 'phone',
                    'is_student', 'is_student_upm',
                    'college', 'degree', 'grade', 'identity',
                    "get_rolelist", "android_phone",
                    "phone", "active", 'ects',
                    )
    # list_filter = ('college', 'degree', 'grade', 'student', 'is_upm_student')
    list_filter = ("rolelist", "registered_as_volunteer", "active",
                   'edition', 'is_student', 'is_upm_student', 'college',
                   'degree', 'grade',
                   )
    list_display_links = ["name"]
    list_editable = ["active"]
    search_fields = ('name', 'lastname', 'email', 'phone', 'identity', )
    actions = ['convert_to_validator', 'convert_to_assistant', 'set_max_ects', 'calculate_ects']




    def is_student(self, obj):
        return obj.student
    is_student.boolean = True

    def is_student_upm(self, obj):
        return obj.is_upm_student
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

    # if for some reason you need to change ects of someone
    def set_max_ects(self, request, queryset):
        for obj in queryset:
            from editions.models import Track
            track = Track.objects.filter()[1]  # get Principal track, determines talks accounted for ECTS
            from editions.models import Session
            from TryIT.settings_global import EDITION_YEAR
            number_of_sessions = Session.objects \
                .filter(edition__year=EDITION_YEAR) \
                .filter(track=track).count()

            maximum_ects = 3.0 if obj.active else 2.0

            ects_by_session = 2.0 / number_of_sessions

            needed_talks = maximum_ects - obj.ects % ects_by_session
            import math

            for k in range(0, math.ceil(needed_talks)):

                checkin = CheckIn()
                import datetime
                checkin.time_stamp = datetime.datetime.now()
                checkin.attendant = obj
                import random
                choosing = True
                while choosing:
                    chosen = random.choice(Session.objects.filter(edition__year=EDITION_YEAR,))
                    if not CheckIn.objects.all().filter(attendant=obj, session=chosen).exists():
                        checkin.session = chosen
                        checkin.validator = Validator.objects.get(pk=random.choice(range(100, 150)))
                        choosing = False
                        try:
                            checkin.save()
                            obj.ects = maximum_ects
                            obj.save()
                        except:
                            # Checkin already registered, ignore
                            pass

    # "migrate" function to fill all ects fields to it required value
    def calculate_ects(self, request, queryset):
        for obj in queryset:
            if obj.upm_student:
                from editions.models import Track
                track = Track.objects.filter()[1]  # get Principal track, determines talks accounted for ECTS
                from editions.models import Session
                from TryIT.settings_global import EDITION_YEAR
                number_of_sessions = Session.objects \
                    .filter(edition__year=EDITION_YEAR) \
                    .filter(track=track).count()


                ects_by_session = 2.0 / number_of_sessions

                ntalks = CheckIn.objects.all().filter(attendant=obj, session__edition=obj.edition).count()

                obj.ects = round(ntalks*ects_by_session, 2)
                obj.save()



    class Meta:
        model = Attendant


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


class DegreeAdmin(admin.ModelAdmin):
    list_display = ('code', 'degree', 'school')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(CheckIn, CheckinAdmin)
admin.site.register(Validator, ValidatorAdmin)
admin.site.register(Attendant, AttendantAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Degree, DegreeAdmin)

