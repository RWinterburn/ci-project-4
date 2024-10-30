# context_processors.py
from .models import CartItem

def cart_items(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.beat.price * item.quantity for item in cart_items)
        return {
            'cart_items': cart_items,
            'cart_item_count': total_quantity,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }
    return {}
