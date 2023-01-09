import uuid as uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase
from taggit.models import TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # This is used so that taggit can work with UUID primary key
    # https://stackoverflow.com/questions/31683216/django-taggit-on-models-with-uuid-as-pk-throwing-out-of-range-on-save
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Place(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=20)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    name = models.CharField(max_length=50, null=True)
    reward_checkin_points = models.IntegerField()
    type = models.CharField(max_length=50)
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)

    def __str__(self):
        return self.name
