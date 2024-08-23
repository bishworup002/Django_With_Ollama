from django.contrib import admin
from .models import Property, Location, Amenity, PropertyImage, PropertySummary
from django.utils.html import format_html, format_html_join


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "get_amenity",
        "get_locations",
        "create_date",
        "update_date",
    )
    search_fields = ["title"]
    filter_horizontal = ("locations", "amenities")

    def get_amenity(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()])

    get_amenity.short_description = "Amenities"

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
    search_fields = ["name"]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)

    class Meta:
        verbose_name = "Amenities"


@admin.register(PropertySummary)
class PropertySummaryAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "summary",
    )
    search_fields = ["property__title"]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("property", "image", "image_View")
    search_fields = ["property__title"]

    def image_View(self, obj):
        if obj.image:
            return format_html(
                f"<img src='{obj.image.url}' width='100' height='100' />"
            )
        return "No Image"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super(PropertyImageAdmin, self).formfield_for_dbfield(
            db_field, request, **kwargs
        )
        if db_field.name == "image" and request.resolver_match.kwargs.get("object_id"):
            # Get the current object
            obj = self.get_object(
                request, request.resolver_match.kwargs.get("object_id")
            )
            if obj and obj.image:
                # Add an HTML image tag to show the current image
                formfield.help_text = format_html(
                    f'<img src="{obj.image.url}" width="200" height="200" style="display: block; margin-bottom: 10px;" />'
                )
        return formfield
