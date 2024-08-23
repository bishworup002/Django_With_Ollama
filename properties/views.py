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


def property_details(request, pk):
    property = get_object_or_404(Property, pk=pk)
    context = {
        "property": property,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "properties/property_detail.html", context)
