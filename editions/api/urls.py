from editions.api.views import UserViewSet, EditionViewSet, CompanyViewSet, TrackViewSet
from django.conf.urls import url, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'editions', EditionViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'tracks', TrackViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
