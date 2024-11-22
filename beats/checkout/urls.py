from django.urls import path
from . import views  # Assuming 'views' contains 'checkout' and other views
from bag.views import view_cart  # Importing 'view_cart' from the 'bag' app

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),

    path('bag/', view_cart, name='bag'),
    
  # Use 'view_cart' from the 'bag' app here
]




