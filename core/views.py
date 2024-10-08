from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment, Product, OrderItem, Cart, CartItem
from .utils import now
from .forms import (
    LoginForm,
    SignupForm,
    SignoutForm,
    PlaceOrderForm, AddToCartForm, CheckoutForm
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import User
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db import transaction
from .utils import get_paynow_client, notify_customer_complete_payment
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib import messages


# Create your views here.


@csrf_exempt
def paynow_webhook(request: HttpRequest, pk=None):
    payment: Payment = get_object_or_404(Payment, pk=pk)
    status = request.POST.get('status', None)
    print("Current status:: ", status)

    status_changed_at = now()

    try:
        if status == Payment.AWAITING_DELIVERY:
            # Update orders
            payment.status = Payment.AWAITING_DELIVERY
            payment.awaiting_delivery_at = status_changed_at
            payment.save()

            # Update orders
            for order in payment.orders.all():
                order.status = Order.AWAITING_DELIVERY
                order.awaiting_delivery_at = status_changed_at
                order.save()

        if status == Payment.PAID:
            # Update payment
            payment.status = Payment.PAID
            payment.paid_at = status_changed_at
            payment.save()

            # Update orders
            for order in payment.orders.all():
                order.status = Order.READY_FOR_DELIVERY
                order.awaiting_delivery_at = status_changed_at
                order.save()

    except Exception as e:
        response = JsonResponse({
            'error': 'Failed to process event'
        })

        response.status_code = 400
        return response

    return JsonResponse({
        'message': 'Webhook processed'
    })


def user_login(request: HttpRequest) -> HttpResponse:
    error = None

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password')
                )
                if user is not None:
                    login(request, user)
                    next = request.GET.get('next', '/')
                    return redirect(next)
                else:
                    error = 'Invalid login credentials'

            except PermissionDenied as e:
                error = 'Invalid login credentials'
        else:
            error = 'Please enter both password and username'

    return render(request, 'core/login.html', {
        'error': error
    })


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignoutForm(request.POST)
        if form.is_valid():
            logout(request)
            return redirect('login')
    # You are not supposed to signout any other way :)
    raise PermissionDenied()


@transaction.atomic
def user_register(request: HttpRequest) -> HttpResponse:
    error = None
    form = SignupForm
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                user: User = User.objects.create_user(
                    first_name=cd.get('first_name'),
                    last_name=cd.get('last_name'),
                    username=cd.get('email'),
                    email=cd.get('email'),
                    password=cd.get('password'),
                    phone=cd.get('phone'),
                    street=cd.get('street'),
                    suburb=cd.get('suburb'),
                    city=cd.get('city'),
                    province=cd.get('province'),
                    house_number=cd.get('house_number'),
                    type=cd.get('role'),
                    lat=cd.get('lat'),
                    lng=cd.get('lng')
                )

                if user is not None:

                    next = request.GET.get('next', '/')
                    if user.type == User.PRODUCER:
                        group = Group.objects.get(name='Producer')
                        user.groups.add(group)
                        user.is_staff = True
                        user.save()
                        next = '/admin'
                    login(request, user)
                    return redirect(next)
                else:
                    error = 'Signup failed'

            except Exception as e:
                error = "Sign up failed"
        else:
            error = 'Enter all required information'

    return render(request, 'core/signup.html', {
        'error': error,
        'form': form
    })


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/index.html', {
    })


class ProductListView(ListView):
    model = Product
    paginate_by = 8

    def get_queryset(self) -> QuerySet[Any]:
        request = self.request
        queryset = Product.objects.all().order_by('-created_at')

        search = request.GET.get('search', None)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        object = self.get_object()
        context['first_image'] = product.image_list.first()
        context['related_products'] = Product.objects.filter(
            user=product.user).exclude(pk=object.pk).order_by('?')[:4]

        try:
            cart_item = CartItem.objects.get(product=product)
        except CartItem.DoesNotExist:
            cart_item = None

        cart_form = AddToCartForm(initial={
            'product': product,
            'quantity': cart_item.quantity if cart_item else 1,
        })

        context['cart_form'] = cart_form

        return context


@login_required
@transaction.atomic
def add_to_cart(request: HttpRequest) -> HttpResponse:
    form = AddToCartForm(request.POST)

    if form.is_valid():
        cart, cart_created = Cart.objects.get_or_create(user=request.user)

        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        if product.in_stock < quantity:
            messages.add_message(request, messages.ERROR, 'Not enough stock')
            return redirect(product)

        # create item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        messages.add_message(request, messages.SUCCESS, 'Product added to cart')
        return redirect(cart_item.product)


@login_required
@transaction.atomic
def update_cart(request: HttpRequest) -> HttpResponse:
    form = AddToCartForm(request.POST)

    if form.is_valid():
        cart, cart_created = Cart.objects.get_or_create(user=request.user)

        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        if product.in_stock < quantity:
            messages.add_message(request, messages.ERROR, 'Not enough stock')
            return redirect('cart')

        # create item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        messages.add_message(request, messages.SUCCESS, 'Cart updated')
        return redirect('cart')


@login_required
def cart(request: HttpRequest) -> HttpResponse:
    cart = Cart.objects.get(user=request.user)
    items = cart.cartitem_set.all()
    for item in items:
        item.form = AddToCartForm(initial={
            'quantity': item.quantity,
            'product': item.product
        })

    checkout_form = CheckoutForm(initial={
        'checkout': 1
    })
    return render(request, 'core/cart.html', {'cart': cart, 'items': items, 'checkout_form': checkout_form})


@login_required
@transaction.atomic
def checkout(request: HttpRequest) -> HttpResponse:
    form = CheckoutForm(request.POST)

    total_payment = 0
    order_ids = []
    orders = []
    if form.is_valid():
        cart = Cart.objects.get(user=request.user)
        items = cart.cartitem_set.all()
        for item in items:
            customer: User = request.user
            order_title = 'Order for ' + customer.first_name + " " + customer.last_name
            order = Order.objects.create(
                customer=customer,
                status=Order.PENDING,
                pending_at=now(),
                title=order_title,
                description=item.product.name,
                producer=item.product.user
            )

            orders.append(order)

            order_ids.append(str(order.pk))

            order_item = OrderItem.objects.create(
                product=item.product,
                quantity=item.quantity,
                order=order
            )

            total_payment += order_item.total()

        CartItem.objects.filter(cart=cart).delete()
        db_payment = Payment.objects.create(
            status=Payment.CREATED,
            amount=order.total(),
            internal_created_at=now(),
            customer=order.customer
        )

        for order in orders:
            db_payment.orders.add(order)

        return_url = settings.SITE_BASE_URL_NGROK + reverse('order_list')
        result_url = settings.SITE_BASE_URL_NGROK + reverse('paynow_webhook', kwargs={'pk': db_payment.pk})

        paynow = get_paynow_client(return_url, result_url)
        email = 'chaulapatrice@gmail.com'

        reference = f'Order #{",".join(order_ids)}'
        payment = paynow.create_payment(reference, email)

        # Add item to payment
        payment.add(
            reference,
            order_item.total()
        )

        response = paynow.send(payment)

        if response.success:
            # update payment
            db_payment.paynow_redirect_url = response.redirect_url
            db_payment.paynow_poll_url = response.poll_url
            db_payment.save()
            # 3. Notify customer to complete payment
            notify_customer_complete_payment(db_payment.customer, db_payment)
            return redirect(db_payment.paynow_redirect_url)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order


class OrderListView(ListView):
    model = Order
    paginate_by = 15

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Order.objects.all().order_by('-created_at')
        queryset = queryset.filter(customer=self.request.user)

        return queryset
