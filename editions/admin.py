from django.contrib import admin

from editions.models import Company, Edition, Speaker, SessionFormat, Session, Track

admin.site.register(Company)
admin.site.register(Edition)
admin.site.register(Speaker)
admin.site.register(SessionFormat)
admin.site.register(Session)
admin.site.register(Track)
