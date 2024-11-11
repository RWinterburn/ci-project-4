# checkout/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.view_cart, name='cart'),
    ]

