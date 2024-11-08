from django.shortcuts import render, redirect
from .models import Order
from instrumentals.models import Beat
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction

# Make sure the view_cart is properly imported if needed
from bag.views import view_cart

from profiles.models import Profile


def checkout(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
    
    # Pass user_profile to the template or use it directly in the view
    context = {
        'profile': user_profile,
        # other checkout data
    }
    return render(request, 'checkout.html', context)
  # Assuming 'instrumentals' is your beats app

