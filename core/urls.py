from django.urls import path
from .views import (
    paynow_webhook,
    user_login,
    user_register,
    user_logout,
    place_order,
    ProductListView,
    ProductDetailView,
    OrderDetailView,
    OrderListView
)

urlpatterns = [
    path('webhook/<int:order_id>', paynow_webhook, name='paynow_webhook'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', user_register, name='register'),
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/order', place_order, name='place_order'),
    path('orders', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
]
