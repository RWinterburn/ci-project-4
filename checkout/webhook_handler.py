from django.http import JsonResponse
from .models import Order
from django.conf import settings
from .forms import OrderForm


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
      
        return JsonResponse({'status': 'success'}, status=200)

    def handle_payment_intent_succeeded(self, event):
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
            
            return JsonResponse({'status': 'success'}, status=200)

        except Order.DoesNotExist:
            
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

        except Exception as e:
            
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

    def handle_payment_intent_payment_failed(self, event):
    
        
        return JsonResponse({'status': 'success'}, status=200)

    def handle_payment_intent_created(self, event):
        
        
        return JsonResponse({'status': 'success'}, status=200)
