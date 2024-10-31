from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from instrumentals.models import Beat
# Create your views here.



def add_to_cart(request, beat_id):
    beat = get_object_or_404(Beat, id=beat_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, beat=beat)
    
    if not created:
        cart_item.quantity += 1  # Increment quantity if the beat is already in the cart
        cart_item.save()
    
    return redirect('view_cart')


# beats/views.py
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.beat.price * item.quantity for item in cart_items)
    
    return render(request, 'instrumentals/cart.html', {'cart_items': cart_items, 'total': total})


