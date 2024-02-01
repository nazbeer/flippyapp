# flippyapp/management/commands/add_dummy_orders.py

from django.core.management.base import BaseCommand
from flippyapp.models import Order, OrderItem, Product

class Command(BaseCommand):
    help = 'Add dummy orders to the flippyapp'

    def handle(self, *args, **options):
        product1 = Product.objects.get(name='Dummy Product 1')
        product2 = Product.objects.get(name='Dummy Product 2')

        order_item_data = [
            {'product': product1, 'bought_quantity': 2, 'total_amount': 21.98},
            {'product': product2, 'bought_quantity': 1, 'total_amount': 24.99},
        ]

        # Create OrderItems
        order_items = [OrderItem.objects.create(**item_data) for item_data in order_item_data]

        # Calculate total_amount by summing the total_amount of each OrderItem
        total_amount = sum(item.total_amount for item in order_items)

        order_data = {
            'order_items': order_items,
        }

        order = Order.objects.create(**order_data)
        order.total_amount = total_amount
        order.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully added dummy orders'))
