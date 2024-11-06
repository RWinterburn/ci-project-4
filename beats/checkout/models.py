from django.conf import settings
from django.db import models
from instrumentals.models import Beat
from profiles.models import Profile
from django.shortcuts import render

def checkout_view(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
    
    # Pass user_profile to the template or use it directly in the view
    context = {
        'profile': user_profile,
        # other checkout data
    }
    return render(request, 'checkout/checkout.html', context)
  # Assuming 'instrumentals' is your beats app

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.beat.title} (Order {self.order.id})"