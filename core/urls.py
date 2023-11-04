from django.urls import path
from .views import (
    paynow_webhook, 
    user_login, 
    index, 
    browse_deals,
    deal_bids,
    deal_view, 
    invite_customer_to_deal, 
    withdraw, 
    user_register,
    user_logout
)

urlpatterns = [
    path('webhook/<int:order_id>', paynow_webhook, name='paynow_webhook'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', user_register, name='register'),
    path('', index, name='dashboard'),
    path('browse/deals', browse_deals, name='browse_deals'),  
    path('deal/<int:pk>', deal_view, name='deal_view'),
     path('deal/<int:pk>/bids', deal_bids, name='deal_bids'),
    path('deal/<int:pk>/invitation', invite_customer_to_deal, name='invite_customer_to_deal'),
    path('withdraw', withdraw, name='withdraw')
]
