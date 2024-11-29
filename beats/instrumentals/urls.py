# instrumentals/urls.py

from django.urls import path

from . import views  # Import views from the current directory


urlpatterns = [
    path('', views.beat_list, name='beats'),  # List all beats
    path('add/', views.add_beat, name='add_beat'),  # Add a new beat
    path('edit/<int:beat_id>/', views.edit_beat, name='edit_beat'),  # Edit an existing beat
    path('delete/<int:beat_id>/', views.delete_beat, name='delete_beat'),  # Delete a beat
]

