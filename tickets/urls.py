from django.conf.urls import url
from tickets import views

urlpatterns = [
    # url(r'^$', view=views.home, name='home'),
    url(r'^$', view=views.tickets, name='tickets'),

    url(r'^create/', view=views.create_ticket, name='create'),
    url(r'^validate/', view=views.validate_ticket, name='validate')
]
