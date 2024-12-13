
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    
    
    client_secret = settings.STRIPE_SECRET_KEY
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError as e:

        
        return JsonResponse({"status": "Invalid payload", "error": str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:

        
        return JsonResponse({"status": "Invalid signature", "error": str(e)}, status=400)
    except Exception as e:

        
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)  


    handler = StripeWH_Handler(request)


    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
        'payment_intent.created': handler.handle_payment_intent_created,
        
    }


    event_type = event['type']


    event_handler = event_map.get(event_type, handler.handle_event)


    response = event_handler(event)
    return response