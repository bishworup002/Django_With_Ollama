from django.contrib import admin
from .models import Property, Location, Amenity, PropertyImage

admin.site.register(Property)
admin.site.register(Location)
admin.site.register(Amenity)
admin.site.register(PropertyImage)
