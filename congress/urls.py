from django.conf import settings
from django.urls import path

from congress import views


app_name = 'reviews'


urlpatterns = [
    path('', view=views.home, name='home'),
    path('contact/', view=views.contact, name='contact'),
    path('last-editions/', view=views.last_editions, name='last-editions'),
    path('streaming/', view=views.streaming, name='streaming'),
    path('streaming/api', view=views.streamingApi.as_view()),
    path('asistencia/', view=views.AttendanceView, name='attendance'),
    path('asistencia/api', view=views.AttendanceApi.as_view())
]

if settings.HASHCODE:
    urlpatterns.append(
        path('hashcode/', view=views.hashcode, name='hashcode')
    )


if settings.STATS:
    urlpatterns.extend([
        path('stats/', view=views.stats, name='stats'),
        path('stats/charts', view=views.stats_charts, name='stats_charts')
    ])

if settings.ACTIVITIES:
    urlpatterns.extend([
        path('activities/', view=views.activities, name='activities'),
    ])
if settings.WORKSHOPS:
    urlpatterns.extend([
        path('workshops/', view=views.workshops, name='workshops'),
    ])
if settings.CONTESTS:
    urlpatterns.extend([
        path('contests/', view=views.contests, name='contests'),
    ])
    

if settings.PRIZES_ACTIVE:
    urlpatterns.extend([
        path('prizes/', view=views.prizes, name='prizes'),
        path('get-winner/', view=views.get_winner, name='get-winner')
    ])
