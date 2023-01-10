from django.contrib import admin

from .models import Place


class PlaceAdmin(admin.ModelAdmin):
    ordering = ['code']
    search_fields = ['type']
    list_display = ["code", "name", "address", "location", "reward_checkin_points", "type", "all_tags"]

    def location(self, place):
        return f"{place.location_lat} - {place.location_lon}"

    def all_tags(self, place):
        tags = []
        for tag in place.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)


admin.site.register(Place, PlaceAdmin)
