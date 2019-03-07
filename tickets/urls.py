from django.conf.urls import url
from django.urls import path
from django.conf import settings

from tickets import views

urlpatterns = [
    # path('$', view=views.home, name='home'),
    path('validate/', view=views.validate_ticket, name='validate')
]

if settings.TICKETS_SALE:
    urlpatterns.append(
        path('', view=views.tickets, name='tickets'),
    )
    urlpatterns.append(
        path('create/', view=views.create_ticket, name='create')
    )