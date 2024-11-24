from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from instrumentals.models import Beat


@login_required
def add_to_cart(request, beat_id):
    beat = get_object_or_404(Beat, id=beat_id)

    # Update the session cart
    bag = request.session.get('bag', {})
    if str(beat.id) in bag:
        bag[str(beat.id)] += 1
    else:
        bag[str(beat.id)] = 1
    request.session['bag'] = bag

    # Update the database cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, beat=beat)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})
    cart_items = []

    # Initialize total price
    total = 0

    # Create a list of items based on the session data
    for beat_id, quantity in bag.items():
        beat = get_object_or_404(Beat, id=beat_id)
        total_price = beat.price * quantity  # Calculate total price for each item
        cart_items.append({'beat': beat, 'quantity': quantity, 'total_price': total_price})
        total += total_price  # Add the total price of the item to the grand total

    return render(request, 'instrumentals/cart.html', {'cart_items': cart_items, 'total_price': total})


