import logging
from django.http import JsonResponse
from .models import Order
from django.conf import settings
from .forms import OrderForm

logger = logging.getLogger(__name__)

class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unexpected webhook event.
        """
        logger.warning(f"Unhandled Webhook event received: {event['type']}")
        return JsonResponse({'status': 'success'}, status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        """
        intent = event['data']['object']  # Contains the PaymentIntent
        stripe_pid = intent.id
        metadata = intent.metadata
    
    
        order_number = metadata.get('order_number')
        

        try:
            # Attempt to retrieve the order by order number
            order = Order.objects.get(order_number=order_number)
            order.stripe_payment_id = stripe_pid
            order.stripe_payment_status = intent.status
            order.stripe_metadata = metadata
            order.save()

            logger.info(f"Order {order_number} updated successfully with payment info.")

            return JsonResponse({'status': 'success'}, status=200)

        except Order.DoesNotExist:
            # Log error if order is not found
            logger.error(f"Order not found for order_number: {order_number}")
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

        except Exception as e:
            # Log any other unexpected errors
            logger.error(f"Error processing payment intent: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe.
        """
        logger.warning(f"Payment failed: {event['data']['object']}")
        return JsonResponse({'status': 'success'}, status=200)

    def handle_payment_intent_created(self, event):
        """
        Handle the payment_intent.created webhook from Stripe.
        """
        logger.info(f"Payment Intent created: {event['data']['object']}")
        return JsonResponse({'status': 'success'}, status=200)
