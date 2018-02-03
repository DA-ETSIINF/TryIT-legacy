from django.conf.urls import url

from register import views

urlpatterns = [
    url(r'^$', view=views.register, name='register'),
    url(r'^send/', view=views.submit, name='send')
]