from django.contrib import admin

from mail import functions
from volunteers.models import Volunteer, VolunteerRole
from .models import Attachment, Mail


# Register your models here.


@admin.register(Mail)
class ManageMail(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ['subject', 'date']
    actions = ['mail_to_validator', 'mail_to_assistant', 'mail_all']

    def mail_to_validator(self, request, queryset):
        for obj in queryset:
            pass

    mail_to_validator.short_description = "Send mail to validator"

    def mail_to_validator(self, request, queryset):
        for obj in queryset:
            validator_role = VolunteerRole.objects.get(role="validator")
            volunteers = Volunteer.objects.filter(rolelist=validator_role, active=True)

            for volunteer in volunteers:
                body = obj.body + '\n\nId: {}\nContraseña: {}'.format(volunteer.validator.id ,volunteer.validator.secret_key)
                functions.mailValidator(obj.subject, body, volunteer.email, obj.attachment)

    mail_to_validator.short_description = "Send mail to validator"

    def mail_to_assistant(self, request, queryset):
        for obj in queryset:
            assistant_role = VolunteerRole.objects.get(role="assistant")
            volunteers = Volunteer.objects.filter(rolelist=assistant_role, active=True)

            mails = [v.email for v in volunteers]
            functions.mailVolunteer(obj.subject, obj.body, mails, obj.attachment)

    mail_to_assistant.short_description = "Send mail to assistant"

    def mail_all(self, request, queryset):
        for obj in queryset:
            volunteers = Volunteer.objects.filter(active=True)

            mails = [v.email for v in volunteers]
            functions.mailVolunteer(obj.subject, obj.body, mails, obj.attachment)

    mail_all.short_description = "Send mail to all"


admin.site.register(Attachment)
