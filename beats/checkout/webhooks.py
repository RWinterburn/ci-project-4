import logging
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .webhook_handler import StripeWH_Handler

# Initialize logger
logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def webhook(request):
    logger.debug("Webhook request received")
    
    client_secret = settings.STRIPE_SECRET_KEY
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {str(e)}")
        return JsonResponse({"status": "Invalid payload", "error": str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Invalid signature: {str(e)}")
        return JsonResponse({"status": "Invalid signature", "error": str(e)}, status=400)
    except Exception as e:
        # Other errors
        logger.error(f"Error: {str(e)}")
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)  # Use 500 for internal server errors

    # Instantiate the handler
    handler = StripeWH_Handler(request)

    # Map Stripe events to handler methods
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
        'payment_intent.created': handler.handle_payment_intent_created,
        # Add more event types as needed
    }

    # Get the type of event
    event_type = event['type']

    # Get the appropriate handler method from the event_map
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler
    response = event_handler(event)
    return response
