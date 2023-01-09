from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from taggit.serializers import TaggitSerializer

from .models import Place


class LocationSerializer(serializers.Serializer):
    lat = serializers.FloatField(source="location_lat")
    lon = serializers.FloatField(source="location_lon")


class PlaceSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    location = LocationSerializer(source="*")
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Place
        fields = [
            "uuid",
            "address",
            "code",
            "location",
            "name",
            "reward_checkin_points",
            "tags",
            "type",
        ]
