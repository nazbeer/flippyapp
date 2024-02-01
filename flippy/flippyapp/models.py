from django.db import models
from django.utils import timezone
from bson import ObjectId
from pymongo import MongoClient

# Assuming you have a MongoDB client instance
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.flippydb

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Address(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.city}, {self.country} - {self.zip_code}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bought_quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.bought_quantity}"

class Order(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    order_items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f"Order - {self.id}"

class OrderWithAddress(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    order_items = models.ManyToManyField(OrderItem)
    total_amount = models.FloatField()
    user_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"OrderWithAddress - {self.id}"

# Add this method to your models to save them to MongoDB
def save_to_mongo(self, collection_name):
    model_data = self.__dict__.copy()
    model_data.pop("_state", None)
    db[collection_name].update_one({'_id': ObjectId(self.id)}, {'$set': model_data}, upsert=True)

# Attach the save_to_mongo method to each model
for model in [Product, Address, OrderItem, Order, OrderWithAddress]:
    setattr(model, 'save_to_mongo', save_to_mongo.__get__(model))
