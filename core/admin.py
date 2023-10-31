from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .forms import ProductForm, ProductRequestForm, AdminWithdrawalForm
from .models import (
    Payment,
    Order,
    OrderItem,
    Product,
    Deal,
    DealItem,
    Payment,
    ProductRequest,
    Withdrawal
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

    readonly_fields = (
        'paynow_redirect_url',
        'paynow_poll_url',
        'amount',
        'status',
        'delivered_at',
        'awaiting_delivery_at',
        'paid_at',
        'paynow_created_at',
        'sent_at',
        'cancelled_at',
        'disputed_at',
        'refunded_at',
        'customer',
        'order'
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = (
        'quantity',
        'product'
    )

    extra = 0

    def has_delete_permission(self, request: HttpRequest, obj: OrderItem | None = None) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest, obj: OrderItem | None = None) -> bool:
        return False


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status'
    )

    readonly_fields = (
        'deal',
        'pending_at',
        'awaiting_delivery_at',
        'delivered_at',
        'ready_for_delivery_at',
        'sent_out_at',
        'cancelled_at',
        'failed_at',
        'customer'
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

    readonly_fields = (
        'accepted_at',
        'completed_at',
        'closed_at',
        'customer'
    )

    inlines = [DealItemInline]

    def has_delete_permission(self, request: HttpRequest, obj: Deal | None = None) -> bool:
        if obj != None:
            if obj.status in [Deal.ACCEPTED, Deal.SEALED, Deal.COMPLETED]:
                return False
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request: HttpRequest, obj: Deal | None = None) -> list[str] | tuple[str]:
        if obj == None:
            return ('status', 'assignee', 'customer', 'accepted_at', 'completed_at', 'closed_at')
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

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'user',
        'paid',
        'paid_at',
        'created_at'
    )

    readonly_fields = (
        'user',
        'amount'
    )
    form = AdminWithdrawalForm
