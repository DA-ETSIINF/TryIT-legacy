from django.conf.urls import url

from congress import views

urlpatterns = [
    url(r'^$', view=views.home, name='home'),
    url(r'^activities/$', view=views.activities, name='activities'),
    url(r'^workshops/$', view=views.workshops, name='workshops'),
    url(r'^contests/$', view=views.contests, name='contests'),
    url(r'^calendar/$', view=views.calendar, name='calendar'),
    url(r'^tickets/$', view=views.tickets, name='tickets'),
    url(r'^contact/$', view=views.contact, name='contact'),
    url(r'^last-editions/$', view=views.last_editions, name='last-editions')
]
