from django.conf.urls import url
from django.urls import path

from tickets import views

urlpatterns = [
    # path('$', view=views.home, name='home'),
    path('', view=views.tickets, name='tickets'),

    path('create/', view=views.create_ticket, name='create'),
    path('validate/', view=views.validate_ticket, name='validate')
]
