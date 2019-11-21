from django.contrib import admin

# Register your models here.
from congress.models import Streaming, Organizers

admin.site.register(Streaming)
admin.site.register(Organizers)
