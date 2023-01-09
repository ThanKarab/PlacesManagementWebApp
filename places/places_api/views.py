from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Place
from .serializers import PlaceSerializer
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter


class PlaceListApiView(ListAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['code']
    search_fields = ['address']

    def post(self, request, *args, **kwargs):
        """
        Create a place with the given data.
        """
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceDetailApiView(APIView):
    def get_object(self, place_uuid):
        """
        Helper method to get the place object with specific uuid.
        """
        try:
            return Place.objects.get(uuid=place_uuid)
        except Place.DoesNotExist:
            return None

    def get(self, request, place_uuid, *args, **kwargs):
        """
        Retrieves the place item with specific uuid, if exists.
        """
        place_instance = self.get_object(place_uuid)
        if not place_instance:
            return Response(
                {"error": "An object with the specified uuid does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PlaceSerializer(place_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, place_uuid, *args, **kwargs):
        """
        Updates the place item with given uuid, if exists.
        """
        place_instance = self.get_object(place_uuid)
        if not place_instance:
            return Response(
                {"error": "An object with the specified uuid does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PlaceSerializer(instance=place_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, place_uuid, *args, **kwargs):
        """
        Deletes the place item with given uuid, if exists.
        """
        place_instance = self.get_object(place_uuid)
        if not place_instance:
            return Response(
                {"error": "An object with the specified uuid does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_data = PlaceSerializer(place_instance).data
        place_instance.delete()
        return Response(serializer_data, status=status.HTTP_200_OK)
