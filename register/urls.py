from django.conf.urls import url

from register import views

urlpatterns = [
    url(r'^send/', views.submit, name='send')
]