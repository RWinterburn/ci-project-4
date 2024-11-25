
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from instrumentals.models import Beat
from profiles.models import Profile
from bag.models import CartItem


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
    path('checkout/', include('checkout.urls')),
    
      # This includes payment_success
]

     
     
  # Include beats app URLs


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
