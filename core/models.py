from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import (
    notify_agent_deal_assigned,
    notify_agent_deal_unassigned,
    notify_customer_complete_payment,
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
        (FAILED, 'failed')
    )

    status = models.CharField(max_length=45, choices=STATUSES, default=PENDING)
    title = models.CharField(max_length=255)
    deal = models.OneToOneField(
        'Deal', null=True, on_delete=models.SET_NULL, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pending_at = models.DateTimeField(null=True, blank=True)
    awaiting_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    ready_for_delivery_at = models.DateTimeField(null=True, blank=True)
    sent_out_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)

    customer = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return "Order #" + str(self.pk)

    def total(self):
        return sum([item.total() for item in self.items.all()])


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


class Deal(models.Model):
    OPEN = 'open'
    ACCEPTED = 'accepted'
    SEALED = 'sealed'
    COMPLETED = 'completed'
    CLOSED = 'closed'
    STATUSES = (
        (OPEN, 'Open'),
        (ACCEPTED, 'Accepted'),
        (SEALED, 'Sealed'),
        (COMPLETED, 'Completed'),
        (CLOSED, 'Closed')
    )

    status = models.CharField(
        max_length=45, choices=STATUSES, default=OPEN)

    title = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    assignee = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assignee')

    customer = models.OneToOneField(
        'users.User', null=True, on_delete=models.SET_NULL, related_name='customer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_assignee = self.assignee

    def __str__(self) -> str:
        return self.title

    def get_admin_url(self):
        return settings.SITE_BASE_URL + reverse('admin:{0}_{1}_change'
                                                .format(self._meta.app_label, self._meta.model_name),
                                                args=(self.pk,))

    def get_commission(self):
        return sum([item.total() for item in self.items.all()]) * 0.1


class DealItem(models.Model):
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deal = models.ForeignKey(
        'Deal', on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='deal_items')

    def total(self):
        return float(self.product.price) * self.quantity


@receiver(post_save, sender=Deal)
def post_save_deal(sender, instance: Deal, created,  **kwargs):
    if created:
        if instance.assignee != None:
            notify_agent_deal_assigned(
                instance.assignee.phone,
                instance.assignee.first_name,
                instance)
    else:
        if instance.old_assignee != None and instance.assignee != None:
            if instance.old_assignee.pk != instance.assignee.pk:

                notify_agent_deal_unassigned(
                    instance.old_assignee.phone,
                    instance.old_assignee.first_name,
                    instance)

                notify_agent_deal_assigned(
                    instance.assignee.phone,
                    instance.assignee.first_name,
                    instance)

        if instance.old_assignee == None and instance.assignee != None:
            notify_agent_deal_assigned(
                instance.assignee.phone,
                instance.assignee.first_name,
                instance)

        if instance.old_assignee != None and instance.assignee == None:
            notify_agent_deal_unassigned(
                instance.old_assignee.phone,
                instance.old_assignee.first_name,
                instance)

    if instance.status == Deal.SEALED and instance.customer != None:
        # 1. Create an order
        try:
            instance.order
        except Exception:
            order = Order.objects.create(
                title="Order for deal - " + "#" +
                str(instance.pk) + " - " + instance.title,
                deal=instance,
                customer=instance.customer
            )

            # 2. Create payment
            paynow = get_paynow_client(
                'https://google.com', 'https://gooogle.com')
            order_number = order.pk
            payment = paynow.create_payment(
                f'Order #{order_number}', order.customer.email)

            for deal_item in instance.items.all():
                item = OrderItem.objects.create(
                    quantity=deal_item.quantity,
                    product=deal_item.product,
                    order=order
                )

                payment.add(item.product.name, item.total())

            response = paynow.send(payment)

            if response.success:
                print(response)
                print("**************************************************************")
                dir(response)
                # Insert payment into the database
                payment = Payment.objects.create(
                    status=Payment.CREATED,
                    order=order,
                    amount=order.total(),
                    internal_created_at=now(),
                    customer=order.customer,
                    paynow_redirect_url=response.redirect_url,
                    paynow_poll_url=response.poll_url
                )
                # 3. Notify customer to complete payment
                notify_customer_complete_payment(payment.customer, payment)


@receiver(post_delete, sender=Deal)
def post_delete_deal(sender, instance: Deal, **kwargs):
    if instance.assignee != None:
        notify_agent_deal_unassigned(
            instance.assignee.phone,
            instance.assignee.first_name,
            instance)


class ProductRequest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='product_requests')

    def __str__(self) -> str:
        return self.name
