from django.conf.urls import url
from attendance import views

urlpatterns = [
    # url(r'^$', view=views.home, name='home'),
    url(r'^$', view=views.attendant_info, name='attendance')
]
