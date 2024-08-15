from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    rating = models.CharField(max_length=10, default='0')
    latitude = models.FloatField()
    longitude = models.FloatField()
    room_type = models.CharField(max_length=255, default='Unknown')
    price = models.CharField(max_length=50, default='0')
    locations = models.ManyToManyField(Location, related_name='properties')
    amenities = models.ManyToManyField(Amenity, related_name='properties')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    image = models.ImageField(upload_to='property_images/')
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.property.title}"