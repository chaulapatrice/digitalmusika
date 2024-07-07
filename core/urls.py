from django.urls import path
from .views import (
    paynow_webhook,
    user_login,
    user_register,
    user_logout,
    ProductListView,
    ProductDetailView,
    OrderDetailView,
    OrderListView,
    add_to_cart,
    update_cart,
    cart,
checkout
)

urlpatterns = [
    path('webhook/<int:pk>', paynow_webhook, name='paynow_webhook'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', user_register, name='register'),
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('orders', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('add-to-cart', add_to_cart, name='add_to_cart'),
    path('update-cart', update_cart, name='update_cart'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
]
