from django.urls import path
from . import views  # Assuming 'views' contains 'checkout' and other views
from bag.views import view_cart
 # Importing 'view_cart' from the 'bag' app

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('payment_success/<order_number>/', views.payment_success, name='payment_success'),
]






