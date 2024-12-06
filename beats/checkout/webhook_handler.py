from django.http import HttpResponse
from .models import Order


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unexpected webhook event.
        """
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        """
        intent = event['data']['object']
        stripe_pid = intent.id
        metadata = intent.metadata
        order_number = metadata.get('order_number')

        try:
            order = Order.objects.get(order_number=order_number)
            order.stripe_payment_id = stripe_pid
            order.stripe_payment_status = intent.status
            order.stripe_metadata = metadata
            order.save()

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Updated order with payment info.',
                status=200
            )
        except Order.DoesNotExist:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order not found.',
                status=404
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

        