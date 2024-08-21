from django.shortcuts import render, get_object_or_404
from .models import Property
from django.conf import settings


def property_list(request):
    properties = Property.objects.all()
    for property in properties:
        property.image = (
            property.images.first()
        )  # Access images using the related_name "images"
    context = {
        "properties": properties,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "properties/property_list.html", context)
