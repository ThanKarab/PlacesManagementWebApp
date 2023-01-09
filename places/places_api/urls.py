from django.urls import path

from .views import (
    PlaceListApiView,
    PlaceDetailApiView
)

urlpatterns = [
    path('api/place', PlaceListApiView.as_view()),
    path('api/place/<uuid:place_uuid>/', PlaceDetailApiView.as_view()),
]
