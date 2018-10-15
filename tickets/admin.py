from django.contrib import admin

from tickets.models import TicketType, Ticket, CheckIn, Validator, Attendant, Degree, School

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
                    'college', 'degree', 'grade', 'identity'
                    )
    # list_filter = ('college', 'degree', 'grade', 'student', 'upm_student')
    list_filter = ('edition',
                   'student',
                   'upm_student', 'college', 'degree', 'grade'
                   )

    search_fields = ('name', 'lastname', 'email', 'phone', 'identity')

    def is_student(self, obj):
        return obj.student
    is_student.boolean = True

    def is_student_upm(self, obj):
        return obj.upm_student
    is_student_upm.boolean = True


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
