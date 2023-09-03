from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import (
    Payment,
    Order,
    OrderItem,
    Product,
    Deal,
    Payment,
    ProductRequest
)
# Register your models here.


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'paynow_id',
        'amount',
        'status'
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status'
    )

    inlines = (OrderItemInline,)


@admin.register(Product)
class ProductModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'in_stock',
        'created_at',
        'updated_at'
    )


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Deal)
class DealModelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status'
    )


@admin.register(ProductRequest)
class ProductRequestModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'updated_at'
    )
