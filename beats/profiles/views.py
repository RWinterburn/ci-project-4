from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order
# Create your views here.


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Fetch the user's orders
    orders = Order.objects.filter(email=request.user.email).order_by('-date')

    return render(request, 'profile.html', {'profile': profile, 'orders': orders})