from django.urls import path
from . import views
from .views import profile, edit_profile, delete_profile

urlpatterns = [
    path('', profile, name='profile'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('profile/delete/<int:user_id>/', views.delete_profile, name='delete_profile'),
]
