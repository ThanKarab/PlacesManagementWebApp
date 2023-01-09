from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PlaceViewSet

router = DefaultRouter()
router.register(r"place", PlaceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
