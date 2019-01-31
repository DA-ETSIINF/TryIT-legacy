from django.conf import settings
from django.urls import path

from congress import views

app_name = 'reviews'


urlpatterns = [
    path('', view=views.home, name='home'),
    path('contact/', view=views.contact, name='contact'),
    path('last-editions/', view=views.last_editions, name='last-editions'),
    path('hashcode/', view=views.hashcode, name='hashcode')
]

if settings.READY_FOR_NEW_ED:
    urlpatterns.extend([
        path('activities/', view=views.activities, name='activities'),
        path('workshops/', view=views.workshops, name='workshops'),
        path('contests/', view=views.contests, name='contests'),
        path('stats/', view=views.stats, name='stats'),
        path('stats/charts', view=views.stats_charts, name='stats_charts')
    ])

if settings.PRIZES_ACTIVE:
    urlpatterns.extend([
        path('prizes/', view=views.prizes, name='prizes'),
        path('get-winner/', view=views.get_winner, name='get-winner')
    ])
