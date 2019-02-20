
from django.urls import path, re_path
from events import views


urlpatterns = [
    re_path(r'escape-room/session/(?P<pk>[0-9]+)/$', views.EscapeRoomAddAttendant.as_view(),
            name='add-attendant'),
    path('escape-room/', views.EscapeRoomIndexView, name='escape-room'),
    path('escape-room/api', views.EscapeRoomSessionsView.as_view(), name='escape-room-api'),
]
