from django.contrib import admin
from editions.models import Company, Edition, Speaker, TrackFormat, Track


admin.site.register(Company)
admin.site.register(Edition)
admin.site.register(Speaker)
admin.site.register(TrackFormat)
admin.site.register(Track)
