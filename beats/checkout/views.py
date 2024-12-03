
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import OrderForm
from instrumentals.models import Beat
from bag.models import CartItem
from .models import Order, OrderLineItem
from django.core.mail import send_mail


# Set your secret key for Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        print('form submitted')
        bag = request.session.get('bag', {})
        form_data = {field: request.POST.get(field) for field in OrderForm.Meta.fields}
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            try:
                # Save the order
                order = order_form.save(commit=False)
                order.save()

                # Create order line items
                for item_id, quantity in bag.items():
                    beat = get_object_or_404(Beat, id=item_id)
                    OrderLineItem.objects.create(order=order, beat=beat, quantity=quantity)

                # Clear the bag
                request.session.pop('bag', None)
                print('works')

                # Create a Stripe PaymentIntent
                grand_total = sum(Beat.objects.get(id=item_id).price * quantity for item_id, quantity in bag.items())
                try:
                    intent = stripe.PaymentIntent.create(
                        amount=int(grand_total * 100), 
                        currency='usd',
                        metadata={'order_id': order.id}  # Attach order_id to the metadata
                    )
                
                    client_secret = intent.client_secret
                except stripe.error.StripeError as e:
                    messages.error(request, f"Payment processing error: {e.user_message}")
                    return redirect('view_cart')
                

                # Redirect to the payment success page
                return redirect(reverse('payment_success', args=[order.order_number]))

            except Exception as e:
                print(e)
                messages.error(request, f"Error processing your order: {e}")
                return redirect('view_cart')
        else:
            print(form.errors)

    # Handle GET requests
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your shopping bag is empty.")
        return redirect('view_cart')

    # Calculate the total and initialize Stripe payment
    grand_total = sum(Beat.objects.get(id=item_id).price * quantity for item_id, quantity in bag.items())
    try:
        intent = stripe.PaymentIntent.create(amount=int(grand_total * 100), currency='gbp')
        client_secret = intent.client_secret
    except stripe.error.StripeError as e:
        messages.error(request, f"Payment processing error: {e.user_message}")
        return redirect('view_cart')

    # Render the checkout page with context
    context = {
        'order_form': OrderForm(),
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }
    return render(request, 'checkout/checkout.html', context)







def payment_success(request, order_number):
    # Fetch the order using the provided order_number
    order = get_object_or_404(Order, order_number=order_number)

    # Optionally handle saving user information (if needed)
    save_info = request.session.get('save_info')

    # Show success message to the user
    messages.success(request, f"Order successfully processed! Your order number is {order_number}.")

    # Fetch the purchased items (order line items) for the order
    purchased_items = OrderLineItem.objects.filter(order=order)

    # Clear the session-based shopping bag if it exists
    if 'bag' in request.session:
        del request.session['bag']

    # Render the success page with the purchased items and order context
    return render(request, 'checkout/payment_success.html', {
        'order': order,
        'purchased_items': purchased_items,
    })

    
    
