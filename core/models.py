from django.db import models
from image_cropping import ImageRatioField

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
    paynow_id = models.CharField(max_length=255)
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

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_payments')
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='order_payments')

    def __str__(self):
        return self.user.username


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pending_at = models.DateTimeField(null=True, blank=True)
    awaiting_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    ready_for_delivery_at = models.DateTimeField(null=True, blank=True)
    sent_out_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return "Order #" + str(self.pk)


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


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    cropping = ImageRatioField('image', '430x360')
    in_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='products')

    def __str__(self) -> str:
        return self.name


class Deal(models.Model):
    UNASSIGNED = 'unassigned'
    ASSIGNED = 'assigned'
    ACCEPTED = 'accepted'
    COMPLETED = 'completed'
    CLOSED = 'closed'
    STATUSES = (
        (UNASSIGNED, 'Unassigned'),
        (ASSIGNED, 'Assigned'),
        (ACCEPTED, 'Accepted'),
        (COMPLETED, 'Completed'),
        (CLOSED, 'Closed')
    )

    status = models.CharField(
        max_length=45, choices=STATUSES, default=UNASSIGNED)

    title = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    unassigned_at = models.DateTimeField(null=True, blank=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    assignee = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, blank=True)

    products = models.ManyToManyField('Product', related_name='deal_products')

    def __str__(self) -> str:
        return self.title


class ProductRequest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_requests')
    cropping = ImageRatioField('image', '430x360')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='product_requests')

    def __str__(self) -> str:
        return self.name
