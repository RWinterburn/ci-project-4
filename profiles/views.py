from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order, OrderLineItem
# Create your views here.


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order, OrderLineItem

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Fetch the user's orders
    orders = Order.objects.filter(email=request.user.email).order_by('-date')

    # Fetch the purchased items for all orders
    purchased_items = OrderLineItem.objects.filter(order__in=orders)

    return render(
        request,
        'profile.html',
        {'profile': profile, 'orders': orders, 'purchased_items': purchased_items},
    )
