from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[("country", "Country"), ("state", "State"), ("city", "City")],
        default="country",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000, blank=True, default="")
    locations = models.ManyToManyField(Location, related_name="properties")
    amenities = models.ManyToManyField(Amenity, related_name="properties")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    image = models.ImageField(upload_to="property_images/")
    property = models.ForeignKey(
        Property, related_name="images", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertySummary(models.Model):
    property = models.OneToOneField(
        Property, on_delete=models.CASCADE, related_name="summary"
    )
    summary = models.TextField()

    def __str__(self):
        return f"Summary for {self.property.title}"
