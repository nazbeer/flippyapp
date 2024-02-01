from django.shortcuts import render, reverse, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bson import ObjectId
from pymongo.errors import PyMongoError
from .serializers import ProductSerializer, AddressSerializer, OrderSerializer, OrderItemSerializer, OrderWithAddressSerializer
from .db_connection import connect_to_mongo
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from pymongo.errors import PyMongoError
import pymongo 


class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            if db is not None:
                min_price = request.GET.get('min_price')
                max_price = request.GET.get('max_price')

                filter_query = {}
                if min_price is not None:
                    filter_query['price__gte'] = float(min_price)
                if max_price is not None:
                    filter_query['price__lte'] = float(max_price)

                products_cursor = db['product'].find(filter_query).sort('created_at', pymongo.DESCENDING)
                
                products = list(products_cursor)
                serializer = ProductSerializer(products, many=True)
                return render(request, 'list_products.html', {'products': serializer.data})
            return Response({'error': 'Failed to connect to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AddressListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            addresses_cursor = db['address'].find()
            addresses = list(addresses_cursor)
            serializer = AddressSerializer(addresses, many=True)
            return render(request, 'address_list_create.html', {'addresses': serializer.data})
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            data = {
                'city': request.data.get('city'),
                'country': request.data.get('country'),
                'zip_code': request.data.get('zip_code'),
            }
            result = db['address'].insert_one(data)
            return Response({'_id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderItemListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            order_items_cursor = db['order_item'].find()
            products_cursor = db['product'].find()

            order_serializer = OrderItemSerializer(list(order_items_cursor), many=True)
            product_serializer = ProductSerializer(list(products_cursor), many=True)

            context = {'order_items': order_serializer.data, 'products': product_serializer.data}
            return render(request, 'order_item_list_create.html', context)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            product_id = request.data.get('product')
            product_instance = db['product'].find_one({'_id': ObjectId(product_id)})
            data = {
                'product': product_instance,
                'bought_quantity': request.data.get('bought_quantity'),
                'total_amount': request.data.get('total_amount')
            }
            result = db['order_item'].insert_one(data)
            return Response({'_id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderCreateView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'order_create.html')

    def post(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                db['order'].insert_one(serializer.validated_data)
                return Response(serializer.validated_data, status=201)
            return Response(serializer.errors, status=400)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderWithAddressCreateView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            order_with_addresses_cursor = db['order_with_address'].find()
            serializer = OrderWithAddressSerializer(list(order_with_addresses_cursor), many=True)
            return render(request, 'order_with_address_list.html', {'order_with_addresses': serializer.data})
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            serializer = OrderWithAddressSerializer(data=request.data)
            if serializer.is_valid():
                db['order_with_address'].insert_one(serializer.validated_data)
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=400)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddNewProductView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'new_product.html')

    def post(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            if db is not None:
                data = {
                    'name': request.POST.get('name'),
                    'price': float(request.POST.get('price')),
                    'quantity': int(request.POST.get('quantity')),
                }
                result = db['product'].insert_one(data)
                return redirect('list-products')
            return Response({'error': 'Failed to connect to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            db = connect_to_mongo()
            url_names = [
                'order-create',
                'list-products',
                'address-list-create',
                'order-item-list-create',
                'order-with-address-list',
                'add-new-product'
            ]
            url_list = [(name, reverse(name)) for name in url_names]
            return render(request, 'home.html', {'urls': url_list})
        except PyMongoError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
