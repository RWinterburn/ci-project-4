# context_processors.py
from instrumentals.models import Beat

def cart_items(request):
    # Initialize totals
    total_quantity = 0
    total_price = 0
    cart_items = []

    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})

    # Calculate totals using the session bag
    for beat_id, quantity in bag.items():
        try:
            beat = Beat.objects.get(id=beat_id)  # Get the beat object
            total_quantity += quantity
            total_price += beat.price * quantity

            # Append each item to the cart items list
            cart_items.append({
                'beat': beat,
                'quantity': quantity,
            })
        except Beat.DoesNotExist:
            continue  # Skip any beat that doesn't exist

    # Return the context with the calculated totals
    return {
        'cart_items': cart_items,
        'cart_item_count': total_quantity,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }