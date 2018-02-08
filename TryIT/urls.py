from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # REST framework authentication
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # editions
    url(r'^editions-api/', include('editions.api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LANDING:
    # register
    urlpatterns.append(url(r'^register/', include('register.urls', namespace='register')))

if settings.TICKETS_SALE:
    # ticket system
    urlpatterns.append(url(r'^tickets/', include('tickets.urls', namespace='tickets')))


if settings.REGISTER_VOLUNTEERS:
    urlpatterns.append(url(r'^volunteers/', include('volunteers.urls', namespace='volunteers')))


# Congress Web URLs
urlpatterns.append(url(r'^', include('congress.urls', namespace='congress')))