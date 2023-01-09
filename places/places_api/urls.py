from django.urls import path

from .views import (
    PlaceListApiView,
    PlaceDetailApiView
)

urlpatterns = [
    path('api', PlaceListApiView.as_view()),
    path('api/<uuid:place_uuid>/', PlaceDetailApiView.as_view()),
]
