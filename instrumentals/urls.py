# instrumentals/urls.py

from django.urls import path

from . import views  


urlpatterns = [
    path('', views.beat_list, name='beats'),  
    path('add/', views.add_beat, name='add_beat'),  
    path('edit/<int:beat_id>/', views.edit_beat, name='edit_beat'),  
    path('delete/<int:beat_id>/', views.delete_beat, name='delete_beat'),  
]

