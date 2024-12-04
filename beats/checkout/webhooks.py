from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .webhook_handler import StripeWH_Handler  # Import your handler class
import stripe
from django.conf import settings

@require_POST
@csrf_exempt
def webhook(request):
    """
    Handle incoming Stripe webhooks.
    """
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        # Invalid payload
        return JsonResponse({"status": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JsonResponse({"status": "Invalid signature"}, status=400)
    except Exception as e:
        # Other errors
        return JsonResponse({"status": "Error", "message": str(e)}, status=400)

    # Instantiate the handler
    handler = StripeWH_Handler(request)

    # Map Stripe events to handler methods
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the type of event
    event_type = event['type']

    # Get the appropriate handler method from the event_map
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler
    response = event_handler(event)
    return response
