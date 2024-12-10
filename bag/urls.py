from django.urls import path

from . import views



urlpatterns = [
    path('add_to_cart/<int:beat_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:beat_id>/', views.remove_from_cart, name='remove_from_cart'),  # Add this
    path('cart/', views.view_cart, name='view_cart'),  # Assuming you have a view_cart view
]

    