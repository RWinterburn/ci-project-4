from django.shortcuts import render, redirect
from .models import Order, OrderItem
from instrumentals.models import Beat
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction

# Make sure the view_cart is properly imported if needed
from bag.views import view_cart

@login_required
def checkout(request):
    user = request.user
    cart = request.session.get('cart', {})  # Get the cart from the session (default to empty dict if not found)
    
    if not cart:
        return redirect('cart')  # Redirect to the cart view if the cart is empty or undefined

    try:
        with transaction.atomic():  # Start a transaction
            order = Order.objects.create(user=user, total_price=0)
            total_price = 0

            for beat_id, quantity in cart.items():
                beat = Beat.objects.get(id=beat_id)
                total_price += beat.price * quantity
                OrderItem.objects.create(order=order, beat=beat, quantity=quantity)

            order.total_price = total_price
            order.save()

            # Send confirmation email
            send_order_confirmation_email(user, order)

        # Clear cart after successful checkout
        request.session['cart'] = {}  # Clear the cart from the session
        return redirect('order_success')  # Make sure this URL name is correct

    except Beat.DoesNotExist:
        # Handle case where a beat is not found
        return redirect('cart')

    except Exception as e:
        # Log the exception and handle it
        print(f"Error during checkout: {e}")
        return redirect('checkout_error')  # Make sure this URL name is correct

def send_order_confirmation_email(user, order):
    subject = "Order Confirmation"
    message = render_to_string('checkout/order_confirmation_email.html', {
        'user': user,
        'order': order
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
