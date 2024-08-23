import psycopg2
from django.core.management.base import BaseCommand
from properties.models import Property, PropertyImage, Location, Amenity
from django.utils import timezone
import requests
from django.core.files.base import ContentFile
from config import SCRAPY_DB  # Import your config


class Command(BaseCommand):
    help = "Migrate data from Scrapy project database to Django"

    # # Scrapy project's database configuration in Config.py
    # SCRAPY_DB = {
    #     "dbname": "trip",  # Replace with your Scrapy DB name
    #     "user": "postgres", # Replace with your user name
    #     "password": "password",# Replace with your user password
    #     "host": "localhost",
    #     "port": "5433",
    # }

    def handle(self, *args, **kwargs):
        # Connect to the Scrapy project's database using the config
        conn = psycopg2.connect(
            dbname=SCRAPY_DB["dbname"],
            user=SCRAPY_DB["user"],
            password=SCRAPY_DB["password"],
            host=SCRAPY_DB["host"],
            port=SCRAPY_DB["port"],
        )
        cur = conn.cursor()

        # Execute a query to fetch data from the Scrapy table
        cur.execute(
            "SELECT title, location, latitude, longitude, image_urls FROM trips"
        )
        rows = cur.fetchall()

        # Migrate each row into the Django Property model
        for row in rows:
            (
                title,
                location_name,
                latitude,
                longitude,
                image_urls,
            ) = row

            # Create or get the Location instance
            location_instance, created = Location.objects.get_or_create(
                name=location_name,
                defaults={
                    "type": "country",  # Default type is country
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )

            # Update location if it was not created (i.e., it already existed)
            if not created:
                location_instance.type = "country"
                location_instance.latitude = latitude
                location_instance.longitude = longitude
                location_instance.save()

            # Create or update the Property instance
            property_instance, created = Property.objects.update_or_create(
                title=title,
                defaults={
                    "description": "",  # Empty description as per new model
                    "create_date": timezone.now(),
                    "update_date": timezone.now(),
                },
            )

            # Clear existing locations and add the correct one
            property_instance.locations.clear()
            property_instance.locations.add(location_instance)

            # Handle the images
            image_urls_list = image_urls.strip("{}").split(",")
            for url in image_urls_list:
                url = url.strip()
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        image_name = url.split("/")[-1]
                        image_instance = PropertyImage(property=property_instance)
                        image_instance.image.save(
                            image_name, ContentFile(response.content), save=True
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to download image {url}: {str(e)}")
                    )

        # Close the cursor and connection
        cur.close()
        conn.close()

        self.stdout.write(
            self.style.SUCCESS("Successfully migrated data from Scrapy to Django!")
        )
