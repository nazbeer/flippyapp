
from django.core.management.base import BaseCommand
from flippyapp.models import Product

class Command(BaseCommand):
    help = 'Add dummy products to the flippyapp'

    def handle(self, *args, **options):
        products_data = [
            {'name': 'Dummy Product 1', 'price': 10.99, 'quantity': 50},
            {'name': 'Dummy Product 2', 'price': 24.99, 'quantity': 30},
            # Add more dummy product data as needed
        ]

        for data in products_data:
            Product.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS('Successfully added dummy products'))
