from django.urls import path
from .views import paynow_webhook

urlpatterns = [
    path('webhook/<int:order_id>', paynow_webhook, name='paynow-webhook')
]