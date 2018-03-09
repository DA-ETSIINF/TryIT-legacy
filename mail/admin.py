from django.contrib import admin
from .models import Attachment, Mail
# Register your models here.


@admin.register(Mail)
class ManageMail(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ['title', 'subject', 'date']


admin.site.register(Attachment)