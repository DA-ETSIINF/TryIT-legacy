from django.urls import path
from . import views

urlpatterns = [
    path('', views.volunteers, name='volunteers'),
    path('send/', view=views.submit, name='send'),
    path('volunteers-time-periods/', view=views.submit, name='send')

]
