from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import (
    notify_agent_deal_assigned,
    notify_agent_deal_unassigned,
    notify_customer_complete_payment,
    notify_agent_deal_completed,
    notify_customer_order_ready,
    get_paynow_client,
    now)
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
# Create your models here.


class Payment(models.Model):
    DELIVERED = 'Delivered'
    AWAITING_DELIVERY = 'Awaiting Delivery'
    PAID = 'Paid'
    CREATED = 'Created'
    SENT = 'Sent'
    CANCELLED = 'Cancelled'
    DISPUTED = 'Disputed'
    REFUNDED = 'Refunded'
    STATUSES = (
        (DELIVERED, DELIVERED),
        (AWAITING_DELIVERY, AWAITING_DELIVERY),
        (PAID, PAID),
        (CREATED, CREATED),
        (SENT, SENT),
        (CANCELLED, CANCELLED),
        (DISPUTED, DISPUTED),
        (REFUNDED, REFUNDED)
    )
    paynow_redirect_url = models.CharField(max_length=255)
    paynow_poll_url = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=45, choices=STATUSES)
    delivered_at = models.DateTimeField(null=True, blank=True)
    awaiting_delivery_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    paynow_created_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    disputed_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    internal_created_at = models.DateTimeField(auto_now_add=True)
    internal_updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='customer_payments')
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='order_payments')

    def __str__(self):
        return str(self.customer) + " Payment - #" + str(self.pk)


class Order(models.Model):
    PENDING = 'pending'
    AWAITING_DELIVERY = 'awaiting-delivery'
    DELIVERED = 'delivered'
    READY_FOR_DELIVERY = 'ready-for-shipping'
    SENT_OUT = 'delivery-in-progress'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

    STATUSES = (
        (PENDING, 'Pending'),
        (AWAITING_DELIVERY, 'Awaiting Delivery'),
        (DELIVERED, 'Delivered'),
        (READY_FOR_DELIVERY, 'Ready For Delivery'),
        (SENT_OUT, 'Sent Out'),
        (CANCELLED, 'Cancelled'),
        (FAILED, 'Failed')
    )

    status = models.CharField(max_length=45, choices=STATUSES, default=PENDING)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pending_at = models.DateTimeField(null=True, blank=True)
    awaiting_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    ready_for_delivery_at = models.DateTimeField(null=True, blank=True)
    sent_out_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    producer = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='producer_orders')

    customer = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return "Order #" + str(self.pk)

    def total(self):
        return sum([item.total() for item in self.items.all()])

    def status_class(self) -> str:
        if self.status == Order.PENDING:
            return 'bg-secondary'
        if self.status == Order.AWAITING_DELIVERY:
            return 'bg-info text-dark'
        if self.status == Order.READY_FOR_DELIVERY:
            return 'bg-info text-dark'
        if self.status == Order.DELIVERED:
            return 'bg-success'
        if self.status == Order.SENT_OUT:
            return 'bg-dark'
        if self.status == Order.FAILED:
            return 'bg-danger'


@receiver(post_save, sender=Order)
def post_save_order(sender, instance: Order, created,  **kwargs):
    if instance.status == Order.AWAITING_DELIVERY:
        notify_customer_order_ready(instance)


class OrderItem(models.Model):
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='ordered_items')
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='items')

    def __str__(self) -> str:
        return self.product.name

    def total(self):
        return float(self.product.price) * self.quantity


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    in_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='products')

    def __str__(self) -> str:
        return self.name + " ( #" + str(self.pk) + " ) -- $"\
            + str(self.price)


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product', related_name='image_list', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductRequest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='product_requests')

    def __str__(self) -> str:
        return self.name


class Withdrawal(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    innbucks_qrcode = models.ImageField(upload_to='withdrawals')
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user) + ' - #' + str(self.pk) + ' - $' + str(self.amount)
