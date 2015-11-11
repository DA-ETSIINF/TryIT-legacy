from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # REST framework authentication
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # editions
    url(r'^editions-api/', include('editions.api.urls')),
    url(r'^editions/', include('editions.urls', namespace='editions')),

    # ticket system
    url(r'^tickets/', include('tickets.urls', namespace='tickets')),
]
