from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order, OrderLineItem
# Create your views here.


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order, OrderLineItem

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order, OrderLineItem

@login_required
def profile(request):
    # Get or create a profile for the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Fetch the user's orders (case-insensitive)
    orders = Order.objects.filter(email__iexact=request.user.email).order_by('-date')

    # Fetch the purchased items for all orders
    purchased_items = OrderLineItem.objects.filter(order__in=orders)

    # Debug logging to check data
    print(f"User email: {request.user.email}")
    print(f"Orders: {orders}")
    print(f"Purchased items: {purchased_items}")

    return render(
        request,
        'profile.html',
        {'profile': profile, 'orders': orders, 'purchased_items': purchased_items},
    )
