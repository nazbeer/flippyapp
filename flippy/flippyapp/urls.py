from django.urls import path
from .views import (
    HomeView,
    ProductListView,
    OrderCreateView,
    AddressListCreateView,
    OrderItemListCreateView,
    OrderWithAddressCreateView,
    AddNewProductView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list-products/', ProductListView.as_view(), name='list-products'),
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('address-list-create/', AddressListCreateView.as_view(), name='address-list-create'),
    path('order-item-list-create/', OrderItemListCreateView.as_view(), name='order-item-list-create'),
    path('order-with-address-list/', OrderWithAddressCreateView.as_view(), name='order-with-address-list'),
    path('add-new-product/', AddNewProductView.as_view(), name='add-new-product'),
]
