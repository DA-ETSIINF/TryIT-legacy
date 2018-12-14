from django.urls import path
from . import views

pathpatterns = [
    path('', views.volunteers, name='volunteers'),
    path('send/', view=views.submit, name='send')
]
