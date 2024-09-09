from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(order):
    subject = f"Order Confirmation #{order.id}"
    message = f"Thank you for your order, {order.user.username}!\nYour order ID is {order.id}."
    recipient_list = [order.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )