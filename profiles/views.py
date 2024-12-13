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

    profile, created = Profile.objects.get_or_create(user=request.user)

    orders = profile.orders.all().order_by('-date')

    purchased_items = OrderLineItem.objects.filter(order__in=orders)

    print(f"User email: {request.user.email}")
    print(f"Orders: {orders}")
    print(f"Purchased items: {purchased_items}")

    return render(
        request,
        'profile.html',
        {'profile': profile, 'orders': orders, 'purchased_items': purchased_items},
    )
