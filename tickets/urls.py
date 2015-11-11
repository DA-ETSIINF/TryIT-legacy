from django.conf.urls import url
from tickets import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^create/', views.create_ticket, name='create'),
    url(r'^validate/', views.validate_ticket, name='validate')
]
