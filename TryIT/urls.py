from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import handler404, handler400
from django.conf.urls.static import static
#handler404 = 'congress.views.home'
#handler400 = 'congress.views.home'


urlpatterns = [


    # Admin
    path('admin/', admin.site.urls),

    # REST framework authentication
    path('api-auth/', include('rest_framework.urls')),

    # editions
    path('editions-api/', include('editions.api.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.REGISTER_COMPANIES:
    # register
    urlpatterns.append(path('register/', include(('register.urls', 'register'),  namespace='register')))

if settings.TICKETS_SALE:
    # ticket system
    urlpatterns.append(path('tickets/', include(('tickets.urls', 'tickets'), namespace='tickets')))

urlpatterns.append(path('attendance/', include(('attendance.urls', 'attendance'), namespace='attendance')))


if settings.REGISTER_VOLUNTEERS:
    urlpatterns.append(path('volunteers/', include(('volunteers.urls', 'volunteers'), namespace='volunteers')))

# Congress Web URLs
urlpatterns.append(path('', include(('congress.urls', 'congress'), namespace='congress')),)

