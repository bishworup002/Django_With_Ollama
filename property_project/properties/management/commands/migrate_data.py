import psycopg2
from django.core.management.base import BaseCommand
from properties.models import Property, PropertyImage, Location
from django.utils import timezone

class Command(BaseCommand):
    help = 'Migrate data from Scrapy project database to Django'

    def handle(self, *args, **kwargs):
        # Connect to the Scrapy project's database
        conn = psycopg2.connect(
            dbname='trip',  # Replace with the actual Scrapy DB name
            user='postgres',
            password='p@stgress',
            host='localhost',
            port='5433'
        )
        cur = conn.cursor()

        # Execute a query to fetch data from the Scrapy table
        cur.execute("SELECT id, title, rating, location, latitude, longitude, room_type, price, image_urls FROM trips")
        rows = cur.fetchall()

        # Migrate each row into the Django Property model
        for row in rows:
            # Unpack the row
            (property_id, title, rating, location, latitude, longitude, room_type, price, image_urls) = row

            # Create or get the Location instance
            location_instance, _ = Location.objects.get_or_create(name=location)

            # Create or update the Property instance
            property_instance, created = Property.objects.update_or_create(
                property_id=property_id,
                defaults={
                    'title': title,
                    'rating': rating,
                    'latitude': latitude,
                    'longitude': longitude,
                    'room_type': room_type,
                    'price': price,
                    'create_date': timezone.now(),
                    'update_date': timezone.now(),
                }
            )

            # Add the location to the property
            property_instance.locations.add(location_instance)

            # Handle the images (assuming image_urls is a string of comma-separated URLs)
            image_urls_list = image_urls.strip('{}').split(',')
            for url in image_urls_list:
                PropertyImage.objects.get_or_create(
                    image=url.strip(),
                    property=property_instance
                )

        # Close the cursor and connection
        cur.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Successfully migrated data from Scrapy to Django!'))