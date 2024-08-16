from django.shortcuts import render, get_object_or_404
from .models import Property


def property_list(request):
    properties = Property.objects.all()
    return render(request, "properties/property_list.html", {"properties": properties})


def property_detail(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    return render(request, "properties/property_detail.html", {"property": property})
