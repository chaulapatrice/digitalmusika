from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .forms import ProductForm, ProductRequestForm
from PIL import Image
from .models import (
    Payment,
    Order,
    OrderItem,
    Product,
    Payment,
    ProductRequest,
    ProductImage
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

    def has_delete_permission(self, request: HttpRequest, obj: OrderItem) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest, obj: OrderItem) -> bool:
        return False


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status'
    )

    readonly_fields = (
        'title',
        'description',
        'pending_at',
        'awaiting_delivery_at',
        'delivered_at',
        'ready_for_delivery_at',
        'sent_out_at',
        'cancelled_at',
        'failed_at',
        'customer',
        'producer'
    )

    inlines = (OrderItemInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)

        if request.user.is_superuser == False:
            queryset = queryset.filter(producer=request.user)

        return queryset


class ProductImageModelAdmin(admin.TabularInline):
    model = ProductImage


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

    inlines = [ProductImageModelAdmin]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)

        if request.user.is_superuser == False:
            queryset = queryset.filter(user=request.user)

        return queryset

    def get_form(self, request, obj=None, **kwargs):
        # Pass the user to the form
        self.form.user = request.user
        kwargs['form'] = self.form

        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):

        obj.save()

        x = form.cleaned_data.get('x')
        y = form.cleaned_data.get('y')
        width = form.cleaned_data.get('width')
        height = form.cleaned_data.get('height')

        # Only crop image when x,y, width and height have been provided
        if x and y and width and height:
            image = Image.open(obj.image)
            cropped_image = image.crop((x, y, width + x, height + y))
            cropped_image.save(obj.image.path)


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(ProductRequest)
class ProductRequestModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'updated_at'
    )
    form = ProductRequestForm
