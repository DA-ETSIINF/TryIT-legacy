
from django.urls import path, re_path
from events import views
from django.conf import settings


urlpatterns = []

if settings.ESCAPE_ROOM:
    urlpatterns.append(
        re_path(r'escape-room/session/(?P<pk>[0-9]+)/$', views.EscapeRoomAddAttendant.as_view(),
                name='add-attendant')
    )
    urlpatterns.append(
        path('escape-room/', views.EscapeRoomIndexView, name='escape-room'),
    )
    urlpatterns.append(
        path('escape-room/api', views.EscapeRoomSessionsView.as_view(), name='escape-room-api')
    )
