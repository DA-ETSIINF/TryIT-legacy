from django.conf.urls import url
from django.urls import path

from register import views

urlpatterns = [
    path('', view=views.register, name='register'),
    path('send/', view=views.submit, name='send')
]