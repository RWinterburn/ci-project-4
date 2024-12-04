from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST 
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_handler

import stripe 


@require_POST
@csrf_exempt
def webhook(request):
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    event = None
    
    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({"status": "error"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
            return HttpResponse(content=e, status=400)

    # Handle the event

    print('Sucess!')
    return HttpResponse(status=200)
    