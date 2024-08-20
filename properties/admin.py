from django.contrib import admin
from .models import Property, Location, Amenity, PropertyImage
from django.utils.html import format_html, format_html_join


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "property_id",
        "title",
        "description",
        "get_amenity",
        "get_locations",  # Display locations as an unordered list
        "create_date",
        "update_date",
    )
    search_fields = ["title"]
    filter_horizontal = ("locations", "amenities")

    def get_amenity(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()])

    get_amenity.short_description = "Amenity"

    def get_locations(self, obj):
        locations = obj.locations.all()
        return format_html(
            "<ol>{}</ol>",
            format_html_join(
                "", "<li>{}</li>", ((location.name,) for location in locations)
            ),
        )

    get_locations.short_description = "Locations"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["description"].required = False
        return form


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "latitude", "longitude")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "image", "thumb")
    search_fields = ["property__title"]

    def thumb(self, obj):
        return format_html(f"<img src='{obj.image.url}' width='100' height='100' />")

    thumb.short_description = "View"
