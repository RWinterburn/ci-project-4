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

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            try:
                # Save the order
                order = order_form.save(commit=False)
                order.user = request.user if request.user.is_authenticated else None
                order.save()

                # Add items from the bag to the order
                for item_id, item_data in bag.items():
                    beat = Beat.objects.get(id=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        beat=beat,
                        quantity=item_data,
                    )

                # Clear the session bag
                del request.session['bag']

                # Redirect to payment success page
                return redirect('payment_success', order_number=order.order_number)

            except Exception as e:
                messages.error(request, f"An error occurred while processing your order: {e}")
                return redirect('view_cart')
        else:
            messages.error(request, 'There was an issue with your form. Please check your details.')
            return redirect('checkout')

    # If the request is not POST, render the checkout page
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'There is nothing in your bag.')
        return redirect('view_cart')

    # Calculate the total price
    grand_total = 0
    for beat_id, quantity in bag.items():
        try:
            beat = Beat.objects.get(id=beat_id)
            grand_total += beat.price * quantity
        except Beat.DoesNotExist:
            messages.error(request, "One or more items in your bag could not be found.")
            return redirect('view_cart')

    # Create the Stripe PaymentIntent
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),  # Convert to cents
            currency='usd',
        )
        client_secret = intent.client_secret
    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {e.user_message}")
        return redirect('view_cart')

    # Render the checkout page
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }

    return render(request, template, context)



def payment_success(request, order_number):
    try:
        order = get_object_or_404(Order, order_number=order_number)
    except Exception:
        messages.error(request, "Invalid order number.")
        return redirect('view_cart')

    messages.success(request, f"Order successfully processed! Your order number is {order_number}.")
    
    # Clear the session-based shopping bag
    if 'bag' in request.session:
        del request.session['bag']

    template = 'payment_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
