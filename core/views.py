from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment, Deal
from .utils import now
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
