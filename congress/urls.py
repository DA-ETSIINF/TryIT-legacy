from django.conf.urls import url
from congress import views


urlpatterns = [
    url(r'^$', view='congress.views.home', name='home'),
    url(r'^activities/$', view=views.activities, name='activities'),
    url(r'^calendar/$', view=views.calendar, name='calendar'),
    url(r'^tickets/$', view=views.tickets, name='tickets'),
    url(r'^contact/$', view=views.contact, name='contact')
]
