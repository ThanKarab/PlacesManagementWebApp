from rest_framework.routers import DefaultRouter

from .views import PlaceViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"place/?", PlaceViewSet)

urlpatterns = router.urls
