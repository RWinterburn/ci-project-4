# instrumentals/urls.py

from django.urls import path

from . import views  # Import views from the current directory

urlpatterns = [
    path('instrumentals/', views.beat_list, name='beats'),
    path('cart/add/<int:beat_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),  # Ensure this name matches 'beats'
]