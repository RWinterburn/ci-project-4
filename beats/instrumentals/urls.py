# instrumentals/urls.py

from django.urls import path

from . import views  # Import views from the current directory

urlpatterns = [
    path('beats/', views.beat_list, name='beats'),  # Ensure this name matches 'beats'
]