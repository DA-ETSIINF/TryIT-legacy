
from django.urls import path, re_path
from events import views


urlpatterns = [
    path('escape-room/', views.EscapeRoomIndexView, name='escape-room'),
    path('escape-room/api', views.EscapeRoomSessionsView.as_view(), name='escape-room-api'),
]
