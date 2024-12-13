from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(user, order):

    subject = f"Your order {order.id} confirmation"
    message = render_to_string('checkout/order_confirmation_email.html', {
        'user': user,
        'order': order,
        'items': order.items.all(),
    })


    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
