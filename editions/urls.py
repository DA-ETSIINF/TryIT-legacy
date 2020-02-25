from django.urls import path, re_path

from editions import views


urlpatterns = [
    path('', views.GetAllEditions.as_view(), name='home'),
    re_path(r'talks/(?P<year>\d{4})/', views.GetTalks.as_view()),
    re_path(r'workshops/(?P<year>\d{4})/', views.GetWorkshops.as_view()),
    re_path(r'events/(?P<year>\d{4})/', views.GetEvents.as_view()),
    re_path(r'organizers/(?P<year>\d{4})/', views.GetOrganizers.as_view()),
    re_path(r'sponsors/(?P<year>\d{4})/', views.GetSponsors.as_view()),

]
