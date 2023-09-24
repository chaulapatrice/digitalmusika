from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .forms import ProductForm, ProductRequestForm
from .models import (
    Payment,
    Order,
    OrderItem,
    Product,
    Deal,
    DealItem,
    Payment,
    ProductRequest
)
# Register your models here.


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'customer',
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
class ProductModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'in_stock',
        'created_at',
        'updated_at'
    )
    form = ProductForm


class ProductInline(admin.TabularInline):
    model = Product


class DealItemInline(admin.TabularInline):
    model = DealItem


@admin.register(Deal)
class DealModelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status'
    )

    inlines = [DealItemInline]

    def has_delete_permission(self, request: HttpRequest, obj: Deal | None = None) -> bool:
        if obj != None:
            if obj.status in [Deal.ACCEPTED, Deal.SEALED, Deal.COMPLETED]:
                return False
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request: HttpRequest, obj: Deal | None = None) -> list[str] | tuple[str]:
        if obj == None:
            return ('status', 'assignee', 'customer')
        else:
            return super().get_readonly_fields(request, obj)


@admin.register(ProductRequest)
class ProductRequestModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'updated_at'
    )
    form = ProductRequestForm
