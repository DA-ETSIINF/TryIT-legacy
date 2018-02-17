from django.conf.urls import url, include
from rest_framework import routers

from editions.api.views import UserViewSet, EditionViewSet, CompanyViewSet, SessionViewSet, YearSessionsViewSet, \
    SchoolViewSet

router = routers.DefaultRouter()
router.register(r'editions', EditionViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'sessions', SessionViewSet, base_name='sessions')
router.register(r'yearsessions', YearSessionsViewSet, base_name='yearsessions')
router.register(r'schools', SchoolViewSet, base_name='schools')

urlpatterns = [
    url(r'^', include(router.urls)),
]
