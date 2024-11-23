from django.urls import path

from . import views

urlpatterns=[
path('bag/add/<int:beat_id>/', views.add_to_cart, name='add_to_cart'),
path('', views.view_cart, name='view_cart')]

    