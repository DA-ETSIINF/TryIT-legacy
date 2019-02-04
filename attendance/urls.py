
from django.urls import path, re_path
from attendance import views


## TODO /waves/shake/2/comment/1/delete/ why this is redirecting, it shouldnt !!! Check for action!!!
## apparently its not removing anything....
urlpatterns = [
    path(r'', views.AttendanceIndexView, name='attendance'),
    re_path(r'(?P<dni>[0-9A-Z].+)/$', views.ListAttendanceECTs.as_view(), name='attendance-checked-sessions'),

]
