
from django.urls import path, re_path
from attendance import views

# About the regex:
    # Will only accept 8 numbers + 1 letter OR 1 letter + 7 numbers + 1 letter
    # NIF letters can only be in this range [TRWAGMYFPDXBNJZSQVHLCKE]
    # First NIE letter can only be in the range [XYZ] the second letter in the range [TRWAGMYFPDXBNJZSQVHLCKE]

urlpatterns = [
    path(r'', views.AttendanceIndexView, name='attendance'),
    re_path(r'(?i)(?P<dni>\d{8}[TRWAGMYFPDXBNJZSQVHLCKE]{1}|[XYZ]{1}\d{7}[TRWAGMYFPDXBNJZSQVHLCKE]{1})&(?P<edition>\d{4})$', views.ListAttendanceECTs.as_view(), name='attendance-checked-sessions'),

]
