from django.urls import path
from . import views  # Assuming 'views' contains 'checkout' and other views
from bag.views import view_cart  # Importing 'view_cart' from the 'bag' app

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('payment_success/<str:order_number>/', views.payment_success, name='payment_success'),  # Ensure this is here,  # Payment success page
    path('bag/', view_cart, name='view_cart'),  # Cart view
]






