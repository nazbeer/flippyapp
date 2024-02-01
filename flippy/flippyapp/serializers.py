from rest_framework import serializers
from .models import Product, Order, OrderItem, Address, OrderWithAddress


class AddressSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    city = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    zip_code = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    product = ProductSerializer()
    bought_quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = Product.objects.get(pk=validated_data['product']['id'])
        instance.bought_quantity = validated_data.get('bought_quantity', instance.bought_quantity)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.save()
        return instance


class OrderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField()
    address = AddressSerializer(allow_null=True)
    order_items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        order_items_data = validated_data.pop('order_items', None)

        order = Order.objects.create(**validated_data)

        if address_data:
            order.address = Address.objects.create(**address_data)
        
        if order_items_data:
            for order_item_data in order_items_data:
                order_item_data['product'] = Product.objects.get(pk=order_item_data['product']['id'])
                OrderItem.objects.create(order=order, **order_item_data)

        return order

    def update(self, instance, validated_data):
        instance.created_on = validated_data.get('created_on', instance.created_on)
        instance.address = Address.objects.create(**validated_data['address']) if validated_data.get('address') else None
        instance.save()

        # Update or create order items
        order_items_data = validated_data.get('order_items', [])
        for order_item_data in order_items_data:
            order_item_data['product'] = Product.objects.get(pk=order_item_data['product']['id'])
            order_item, created = OrderItem.objects.update_or_create(order=instance, product=order_item_data['product'], defaults=order_item_data)

        return instance


class OrderWithAddressSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField()
    order_items = OrderItemSerializer(many=True)
    total_amount = serializers.FloatField()
    user_address = AddressSerializer()

    def create(self, validated_data):
        user_address_data = validated_data.pop('user_address', None)
        order_items_data = validated_data.pop('order_items', None)

        order_with_address = OrderWithAddress.objects.create(**validated_data)

        if user_address_data:
            order_with_address.user_address = Address.objects.create(**user_address_data)

        if order_items_data:
            for order_item_data in order_items_data:
                order_item_data['product'] = Product.objects.get(pk=order_item_data['product']['id'])
                OrderItem.objects.create(order_with_address=order_with_address, **order_item_data)

        return order_with_address

    def update(self, instance, validated_data):
        instance.created_on = validated_data.get('created_on', instance.created_on)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.user_address = Address.objects.create(**validated_data['user_address']) if validated_data.get('user_address') else None
        instance.save()

        # Update or create order items
        order_items_data = validated_data.get('order_items', [])
        for order_item_data in order_items_data:
            order_item_data['product'] = Product.objects.get(pk=order_item_data['product']['id'])
            order_item, created = OrderItem.objects.update_or_create(order_with_address=instance, product=order_item_data['product'], defaults=order_item_data)

        return instance
