from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Congress Web URLs
    url(r'^', include('congress.urls', namespace='congress')),

    # REST framework authentication
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # editions
    url(r'^editions-api/', include('editions.api.urls')),
    url(r'^editions/', include('editions.urls', namespace='editions')),

    # ticket system
    url(r'^tickets/', include('tickets.urls', namespace='tickets')),

    # register
    url(r'^tickets/', include('register.urls', namespace='register')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
