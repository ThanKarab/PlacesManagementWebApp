from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Place
from .serializers import PlaceSerializer
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ["code"]
    search_fields = ["address"]

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Deletes the place item with given uuid, if exists.
        """
        place_instance = self.get_object()
        if not place_instance:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        response_body = PlaceSerializer(place_instance).data

        response = super(PlaceViewSet, self).destroy(request, pk, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(response_body, status.HTTP_200_OK)
        else:
            return response
