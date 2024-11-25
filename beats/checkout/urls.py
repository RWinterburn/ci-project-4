from django.urls import path
  # Assuming 'views' contains 'checkout' and other views
from . import views
 # Importing 'view_cart' from the 'bag' app

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/<str:order_number>/', views.payment_success, name='payment_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]







