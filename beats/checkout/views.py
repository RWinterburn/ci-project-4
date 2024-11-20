import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import Beat

# Set your secret key for Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



def checkout(request):
    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})

    # If the bag is empty, redirect to the 'view_cart' page with an error message
    if not bag:
        messages.error(request, 'There is nothing in your bag')
        return redirect('view_cart')  # Redirect to 'view_cart' page

    # Calculate the total price of all the items in the cart
    grand_total = 0
    for beat_id, quantity in bag.items():
        beat = Beat.objects.get(id=beat_id)  # Get the beat object using the ID from the session
        grand_total += beat.price * quantity  # Add the total price of each beat to grand_total

    # Try creating a Stripe PaymentIntent to get the client secret
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),  # Total amount in cents
            currency='usd',
        )
        client_secret = intent.client_secret  # Extract the client secret
    except stripe.error.StripeError as e:
        # Catch Stripe errors and display a message to the user
        messages.error(request, f"Stripe error: {e.user_message}")
        return redirect('view_cart')  # Redirect to the cart if there's an error

    # Create the order form instance
    order_form = OrderForm()

    # Define the template path and context
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,  # Pass the client secret to the frontend
    }

    # Render the checkout template
    return render(request, template, context)

