# myapp/management/commands/generate_dummy_data.py
import random
from django.core.management.base import BaseCommand
from faker import Faker
from flippyapp.models import OrderWithAddress, Address, Product

fake = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for OrderWithAddress model'

    def handle(self, *args, **options):
        # Clear existing data
        OrderWithAddress.objects.all().delete()

        # Create dummy addresses
        addresses = [Address.objects.create(
            city=fake.city(),
            country=fake.country(),
            zip_code=fake.zipcode(),
        ) for _ in range(5)]

        # Create dummy products
        products = [Product.objects.create(
            name=fake.word(),
            # Add other fields as needed
        ) for _ in range(10)]

        # Create dummy OrderWithAddress instances
        for _ in range(20):
            order_items = []
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                order_items.append({
                    'product': product,
                    'bought_quantity': random.randint(1, 10),
                    'total_amount': random.uniform(10, 100),
                })

            OrderWithAddress.objects.create(
                created_on=fake.date_time_this_decade(),
                order_items=order_items,
                total_amount=sum(item['total_amount'] for item in order_items),
                user_address=random.choice(addresses),
            )

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully'))
