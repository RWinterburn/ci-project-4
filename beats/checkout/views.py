import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from instrumentals.models import Beat

# Assuming your Stripe secret key is set in settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, 'There is nothing in your bag')
        return redirect('view_cart')  # Redirect to 'view_cart' page

    # Calculate the total price of all the items in the cart
    grand_total = 0
    beats = []  # To hold beat instances
    for beat_id, quantity in bag.items():
        beat = Beat.objects.get(id=beat_id)  # Get the beat object using the ID from the session
        grand_total += beat.price * quantity  # Add the total price of each beat to grand_total
        beats.append((beat, quantity))

    # Try creating a Stripe PaymentIntent to get the client secret
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),  # Total amount in cents
            currency='usd',
        )
        client_secret = intent.client_secret  # Extract the client secret
    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {e.user_message}")
        return redirect('view_cart')  # Redirect to the cart if there's an error

    # Handle order creation after Stripe payment is confirmed
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.grand_total = grand_total
            order.save()  # Save the order first to generate an order ID

            # Create line items for the order
            for beat, quantity in beats:
                OrderLineItem.objects.create(
                    order=order,
                    product=beat,
                    quantity=quantity,
                    lineitem_total=beat.price * quantity,
                )

            # Store the order number in the session
            request.session['order_number'] = order.order_number

            # Clear the session-based bag
            request.session['bag'] = {}

            # Redirect to payment success
            return redirect('payment_success')

    else:
        order_form = OrderForm()

    # Render the checkout template
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }
    return render(request, template, context)


def payment_success(request):
    # Retrieve cart items from the session or database
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Your bag is empty')
        return redirect('view_cart')

    # Check if the order already exists (from checkout view or session)
    order_number = request.session.get('order_number')  # Assuming order number is stored in session
    if not order_number:
        messages.error(request, 'Order not found')
        return redirect('view_cart')

    try:
        # Retrieve the order using the order_number from session
        order = Order.objects.get(order_number=order_number)

        # Create OrderLineItems for each item in the cart if not already created
        for beat_id, quantity in bag.items():
            beat = Beat.objects.get(id=beat_id)
            if not order.lineitems.filter(product=beat).exists():
                OrderLineItem.objects.create(
                    order=order,
                    product=beat,
                    quantity=quantity,
                    lineitem_total=beat.price * quantity,
                )

        # Update order total and grand total
        order.update_total()
        order.save()

        # Optionally, clear the cart session
        if 'bag' in request.session:
            del request.session['bag']

        # Redirect to success page
        return redirect('payment_success')

    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('view_cart')
