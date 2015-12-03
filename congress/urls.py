from django.conf.urls import url


urlpatterns = [
    url(r'^$', view='congress.views.home', name='home'),
    url(r'^activities/$', view='congress.views.activities', name='activities'),
    url(r'^calendar/$', view='congress.views.calendar', name='calendar'),
    url(r'^tickets/$', view='congress.views.tickets', name='tickets'),
    url(r'^contact/$', view='congress.views.contact', name='contact')
]
