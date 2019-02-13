
from django.urls import path, re_path
from attendance import views

urlpatterns = [
    path(r'', views.AttendanceIndexView, name='attendance'),
    re_path(r'(?P<dni>[0-9A-Z].+)/$', views.ListAttendanceECTs.as_view(), name='attendance-checked-sessions'),

]
