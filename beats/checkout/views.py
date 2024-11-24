
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from instrumentals.models import Beat
from bag.models import CartItem
from .models import Order, OrderLineItem

# Set your secret key for Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {field: request.POST.get(field) for field in OrderForm.Meta.fields}
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            try:
                order = order_form.save(commit=False)
                order.save()

                for item_id, quantity in bag.items():
                    beat = get_object_or_404(Beat, id=item_id)
                    OrderLineItem.objects.create(order=order, beat=beat, quantity=quantity)

                request.session.pop('bag', None)

                # Create PaymentIntent
                grand_total = sum(Beat.objects.get(id=item_id).price * quantity for item_id, quantity in bag.items())
                intent = stripe.PaymentIntent.create(
                    amount=int(grand_total * 100),
                    currency='usd',
                    metadata={'order_number': order.order_number}
                )

                context = {
                    'order_form': OrderForm(),
                    'grand_total': grand_total,
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                    'client_secret': intent.client_secret,
                }
                return render(request, 'checkout/checkout.html', context)

            except Exception as e:
                messages.error(request, f"Error processing your order: {e}")
                return redirect('view_cart')

    return redirect('view_cart')


def payment_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    request.session.pop('bag', None)
    messages.success(request, f"Order successfully processed! Your order number is {order_number}.")
    return render(request, 'checkout/payment_success.html', {'order': order})

    
def stripe_webhook(request):
    # Retrieve the webhook secret from settings
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    # Read the payload from Stripe
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Verify and construct the event
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    # Add more event types if needed
    else:
        print(f"Unhandled event type {event['type']}")

    return JsonResponse({'status': 'success'})