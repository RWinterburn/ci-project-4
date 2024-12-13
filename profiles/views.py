from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, User
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


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('profile')
    return render(request, 'edit_profile.html', {'profile': profile})


@login_required
def delete_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('home')  
    return render(request, 'delete_profile.html', {'profile': profile})