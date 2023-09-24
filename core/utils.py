from twilio.rest import Client
from django.conf import settings
from paynow import Paynow
from datetime import datetime
import pytz


def get_twilio_client() -> Client:
    return Client(settings.TWILIIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def get_paynow_client(return_url: str, result_url: str) -> Paynow:
    return Paynow(
        settings.PAYNOW_INTEGRATION_ID,
        settings.PAYNOW_INTEGRATION_KEY,
        return_url,
        result_url
    )


def send_text_message(phone_number: str, message: str) -> bool:

    if settings.DEBUG:
        phone_number_to = '+27768552976'
    else:
        phone_number_to = phone_number
    client = get_twilio_client()
    try:
        client.messages.create(
            from_='+12562865819',
            body=message,
            to=phone_number_to)
        return True
    except Exception as e:
        return False


def notify_agent_deal_assigned(phone_number: str, first_name: str, deal):
    deal_url = deal.get_admin_url()
    deal_title = deal.title
    deal_id = deal.pk
    payout = deal.get_commission()
    send_text_message(
        phone_number,
        f'Dear {first_name}, congratulations on getting a deal - #{deal_id} - {deal_title}. '
        'Here are the steps to fulfill a deal\n\n'
        '1. Look for a customer\n'
        '2. Get the customer to buy\n'
        '3. Update deal status to "Accepted"\n'
        '4. Wait for the deal to be in "Completed" state\n'
        f'5. Get paid ${payout} \n\n'
        f'What are you waiting for? Go ahead and accept the deal here {deal_url}'
    )


def notify_agent_deal_unassigned(phone_number: str, first_name: str, deal):
    deal_id = deal.pk
    deal_title = deal.title

    send_text_message(
        phone_number,
        f'Dear {first_name}, we regret to inform you that you have been unassigned'
        f' from deal #{deal_id} - {deal_title}'
    )


def notify_customer_complete_payment(customer, payment):
    payment_link = payment.paynow_redirect_url
    first_name = customer.first_name
    phone_number = customer.phone
    order_number = payment.order.pk

    send_text_message(
        phone_number,
        f'Dear {first_name}, order #{order_number} has been created for you on your request. \n'
        f'To fulfill the order please complete payment using the link provided\n\n'
        f'{payment_link}'
    )


def now():
    return datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
