from django.urls import path
from . import views

urlpatterns = [
    path("", views.property_list, name="property_list"),
    path("property/<int:pk>/", views.property_details, name="property_details"),
]
