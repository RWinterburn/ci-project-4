# checkout/views.py
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from instrumentals.models import Beat
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@login_required
def checkout(request):
    user = request.user
    cart = request.session.get('cart', {})  # Assume a session-based cart
    if not cart:
        return redirect('cart')  # Redirect to cart if empty

    # Create an order and calculate total price
    order = Order.objects.create(user=user, total_price=0)
    total_price = 0

    for beat_id, quantity in cart.items():
        beat = Beat.objects.get(id=beat_id)
        total_price += beat.price * quantity
        OrderItem.objects.create(order=order, beat=beat, quantity=quantity)

    # Update order total price
    order.total_price = total_price
    order.save()

    # Send confirmation email with download links
    send_order_confirmation_email(user, order)

    # Clear cart after successful checkout
    request.session['cart'] = {}

    return redirect('order_success')


# Create your views here.

