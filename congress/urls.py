from django.conf import settings
from django.conf.urls import url

from congress import views

urlpatterns = [
    url(r'^$', view=views.home, name='home'),
    url(r'^contact/$', view=views.contact, name='contact'),
    url(r'^last-editions/$', view=views.last_editions, name='last-editions'),
    url(r'^hashcode/$', view=views.hashcode, name='hashcode')
]

if settings.READY_FOR_NEW_ED:
    urlpatterns.extend([
        url(r'^activities/$', view=views.activities, name='activities'),
        url(r'^workshops/$', view=views.workshops, name='workshops'),
        url(r'^contests/$', view=views.contests, name='contests'),
        url(r'^stats/$', view=views.stats, name='stats'),
        url(r'^stats/charts$', view=views.stats_charts, name='stats_charts')
    ])

if settings.PRIZES_ACTIVE:
    urlpatterns.extend([
        url(r'^prizes/$', view=views.prizes, name='prizes'),
        url(r'^get-winner/$', view=views.get_winner, name='get-winner')
    ])
