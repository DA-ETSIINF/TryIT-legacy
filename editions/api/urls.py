from django.urls import path, include
from rest_framework import routers

from editions.api.views import EditionViewSet, CompanyViewSet, SessionViewSet, YearSessionsViewSet, \
    SchoolViewSet

router = routers.DefaultRouter()
router.register(r'editions', EditionViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'sessions', SessionViewSet, )
router.register(r'yearsessions', YearSessionsViewSet,)
router.register(r'schools', SchoolViewSet,)

urlpatterns = [
   path('', include(router.urls)),
]
