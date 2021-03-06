from django.contrib import admin

# Register your models here.
from congress.models import AttendanceSlot, Streaming, Attendance

admin.site.register(Streaming)
admin.site.register(AttendanceSlot)
admin.site.register(Attendance)