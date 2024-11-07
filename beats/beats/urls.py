"""
URL configuration for beats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from instrumentals.models import Beat
from bag.models import CartItem  # Correct

from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),           # Root URL
    path('home/', views.home, name='home'),       # Distinct path for home
    path('about/', views.about, name='about'),
    path('accounts/', include('allauth.urls')),   # Include allauth URLs
     path('instrumentals/', include('instrumentals.urls')),
     path('search/', views.search, name='search'), 
     path('profiles/', include('profiles.urls')), 
     path('bag/', include('bag.urls')),
     path('checkout/', include('checkout.urls')),  # Include beats app URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
