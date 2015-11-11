from django.conf.urls import url
from editions import views


urlpatterns = [
    url(r'^$', views.home, name='home')
]
