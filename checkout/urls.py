from django.urls import path
  # Assuming 'views' contains 'checkout' and other views
from . import views
from .webhooks import webhook

 # Importing 'view_cart' from the 'bag' app

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/<str:order_number>/', views.payment_success, name='payment_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),

]







