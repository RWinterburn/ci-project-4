from instrumentals.models import Beat

def cart_items(request):

    total_quantity = 0
    total_price = 0
    cart_items = []


    bag = request.session.get('bag', {})


    for beat_id, quantity in bag.items():
        try:
            beat = Beat.objects.get(id=beat_id)  
            total_quantity += quantity
            total_price += beat.price * quantity


            cart_items.append({
                'beat': beat,
                'quantity': quantity,
            })
        except Beat.DoesNotExist:
            continue  


    return {
        'cart_items': cart_items,
        'cart_item_count': total_quantity,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }