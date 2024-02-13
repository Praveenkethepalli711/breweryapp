import requests
from django.core.management.base import BaseCommand
from rating.models import Brewery  # Replace 'myapp' with the actual name of your Django app
import uuid

class Command(BaseCommand):
    help = 'Fetch data from API and populate Product model'

    def handle(self, *args, **options):
        api_url = 'https://api.openbrewerydb.org/v1/breweries'

        # Fetch data from the API
        response = requests.get(api_url)

        if response.status_code == 200:
            breweries_data = response.json()

            # Clear existing data in the Product model
            Brewery.objects.all().delete()

            # Populate the Product model with data from the API
            for brewery_data in breweries_data:
                Brewery.objects.create(
                id=uuid.UUID(brewery_data['id']),
                name=brewery_data['name'],
                brewery_type=brewery_data['brewery_type'],
                address_1=brewery_data['address_1'],
                phone=brewery_data['phone']
            )

            self.stdout.write(self.style.SUCCESS('Data successfully imported'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from API. Status code: {response.status_code}'))

