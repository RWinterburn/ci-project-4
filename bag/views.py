from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from instrumentals.models import Beat
from instrumentals.views import beat_list

beats = Beat.objects.all()

from django.shortcuts import redirect

@login_required
def add_to_cart(request, beat_id):
    beat = get_object_or_404(Beat, id=beat_id)

    bag = request.session.get('bag', {})
    if str(beat.id) in bag:
        bag[str(beat.id)] += 1
    else:
        bag[str(beat.id)] = 1
    request.session['bag'] = bag


    cart_item, created = CartItem.objects.get_or_create(user=request.user, beat=beat)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('beats')  

@login_required
def remove_from_cart(request, beat_id):
    beat = get_object_or_404(Beat, id=beat_id)


    bag = request.session.get('bag', {})
    if str(beat.id) in bag:
        del bag[str(beat.id)]
        request.session['bag'] = bag

    CartItem.objects.filter(user=request.user, beat=beat).delete()


    return redirect('view_cart') 


@login_required
def view_cart(request):
    bag = request.session.get('bag', {})
    cart_items = []

    total = 0


    for beat_id, quantity in bag.items():
        beat = get_object_or_404(Beat, id=beat_id)
        total_price = beat.price * quantity  
        cart_items.append({'beat': beat, 'quantity': quantity, 'total_price': total_price})
        total += total_price  

    return render(request, 'instrumentals/cart.html', {'cart_items': cart_items, 'total_price': total})


