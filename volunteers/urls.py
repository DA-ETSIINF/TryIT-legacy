from django.conf.urls import url

from editions import views

urlpatterns = [
    url(r'^$', views.volunteers, name='volunteers'),
    url(r'^send/', view=views.submit, name='send')
]
