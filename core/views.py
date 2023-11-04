from django.shortcuts import render, get_object_or_404, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment, Deal, Withdrawal, DealBid
from .utils import now
from .forms import (
    LoginForm, 
    SignupForm, 
    WithdrawalForm, 
    AcceptDealForm, 
    SignoutForm,
    DealFilterForm,
    AddDealBidForm
)
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from users.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
# Create your views here.


@csrf_exempt
def paynow_webhook(request: HttpRequest, order_id=None):
    order: Order = get_object_or_404(Order, pk=order_id)
    status = request.POST.get('status', None)
    print("Current status:: ", status)

    status_changed_at = now()
    try:
        if status == Payment.AWAITING_DELIVERY:

            # Update payment
            payment = Payment.objects.get(order__id=order.pk)
            payment.status = Payment.AWAITING_DELIVERY
            payment.awaiting_delivery_at = status_changed_at
            payment.save()

            # Update order
            order.status = Order.AWAITING_DELIVERY
            order.awaiting_delivery_at = status_changed_at
            order.save()

            # Update deal
            deal = Deal.objects.get(order__id=order.pk)
            deal.status = Deal.COMPLETED
            deal.completed_at = status_changed_at
            deal.save()

        if status == Payment.PAID:
            # Update payment
            payment = Payment.objects.get(order__id=order.pk)
            payment.status = Payment.PAID
            payment.paid_at = status_changed_at
            payment.save()

            # Update order
            order.status = Order.AWAITING_DELIVERY
            order.awaiting_delivery_at = status_changed_at
            order.save()

            # Update deal
            deal = Deal.objects.get(order__id=order.pk)
            deal.status = Deal.COMPLETED
            deal.completed_at = status_changed_at
            deal.save()

    except Exception as e:
        print("Error::", e)
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
                user = User.objects.create_user(
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
                    house_number=cd.get('house_number')
                )
           
                if user is not None:
                    login(request, user)
                    next = request.GET.get('next', '/')
                    return redirect(next)
                else:
                    error = 'Signup failed'

            except Exception as e:
                error = 'Signup failed'
        else:
            error = 'Enter all required information'

    return render(request, 'core/signup.html', {
        'error': error,
        'form': form
    })



@login_required
def index(request: HttpRequest) -> HttpResponse:

    deals = Deal.objects.filter(assignee=request.user)
    withdrawals = Withdrawal.objects.filter(paid=False, user=request.user)
    payout = sum([withdrawal.amount for withdrawal in withdrawals])

    return render(request, 'core/index.html', {
        'deals': deals,
        'payout': payout
    })

@login_required
def browse_deals(request: HttpRequest) -> HttpResponse:
    deals = Deal.objects.filter(status=Deal.OPEN)
    form = DealFilterForm(request.GET)

    if form.data.get('search'):
        deals = Deal.objects.filter(
            Q(title__icontains=form.data.get('search')) | Q(description__icontains=form.data.get('search')))
    
    return render(request, 'core/deal_list.html', {
        'deals': deals,
        'form': form
    })

@login_required
def deal_bids(request: HttpRequest, pk=None) -> HttpResponse:
    deal = get_object_or_404(Deal, pk=pk)

    form = AddDealBidForm()

    user = request.user


    if request.method == 'POST':
        form = AddDealBidForm(request.POST)

        if form.is_valid():
            DealBid.objects.create(
                user=user,
                deal=deal,
                offer_description=form.cleaned_data.get('offer_description')
            )
    
    bids = DealBid.objects.filter(deal=deal)

    return render(request, 'core/deal_bids.html', {
        'deal': deal,
        'bids': bids,
        'form': form,
    })

@login_required
def deal_view(request: HttpRequest, pk=None) -> HttpResponse:
    deal = get_object_or_404(Deal, pk=pk)

    return render(request, 'core/deal_view.html', {
        'deal': deal
    })

@login_required
def invite_customer_to_deal(request: HttpRequest, pk=None) -> HttpResponse:
    deal = get_object_or_404(Deal, pk=pk)
    form = AcceptDealForm()
    customer = request.user
    error = None
    accepted_deal = deal.status == Deal.ACCEPTED
    deal_taken_byother = False

    if deal.status == Deal.ACCEPTED and deal.customer:
        if deal.customer.pk != customer.pk:
            deal_taken_byother = True
        

    if request.method == 'POST':
        form = AcceptDealForm(request.POST)        
        if form.is_valid():
            try:
                deal.status = Deal.ACCEPTED
                deal.accepted_at = now()
                deal.customer = customer
                deal.save()
                accepted_deal = True
            except Exception as e:
                error = 'Failed to accept deal'
                raise e
        
           

    return render(request, 'core/invite_customer_to_deal.html', {
        'form': form,
        'customer': customer,
        'deal': deal,
        'error': error,
        'accepted_deal': accepted_deal,
        'deal_taken_byother': deal_taken_byother
    })

@login_required
def withdraw(request: HttpRequest) -> HttpResponse:
    form = WithdrawalForm()
    user: User = request.user
    error = None
    message = None
    remaining_balance = user.balance
    withdrawal = None
    withdrawals = Withdrawal.objects.filter(user=user)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, request.FILES)

        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            innbucks_qrcode = form.cleaned_data.get('innbucks_qrcode')
            if amount >= 10.00:
                if amount > (user.balance):
                    error = 'Insufficient balance'
                else:
                    withdrawal = Withdrawal.objects.create(
                        user=user,
                        amount=amount,
                        innbucks_qrcode=innbucks_qrcode
                    )
                    remaining_balance = user.balance  - amount
                    user.balance = remaining_balance
                    user.save()
            else:
                error = 'You can only withdraw $10 and above'
    
    return render(request, 'core/withdraw.html', {
        'error': error,
        'message': message,
        'remaining_balance': remaining_balance,
        'withdrawal': withdrawal,
        'form': form,
        'withdrawals': withdrawals
    })


