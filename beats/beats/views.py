from django.shortcuts import render
from instrumentals.models import Beat
from django.db.models import Q 
from bag.models import CartItem
from checkout.views import payment_success
 # Adjust this import based on your project structure

from profiles.models import Profile

def index(request):
    return render(request, 'home.html')  # This will render 'home.html', which can extend 'base.html'

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# views.py


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.beat.price * item.quantity
    return render(request, 'instrumentals/cart.html', {'cart_items': cart_items})


# beats/views.py


def search(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    beats = Beat.objects.filter(
        Q(title__icontains=query) |
        Q(producer__icontains=query) |
        Q(description__icontains=query) |
        Q(price__icontains=query)
    ) if query else Beat.objects.all()  # Filter beats by multiple fields
    return render(request, 'search.html', {'beats': beats, 'query': query})


def beatlist(request):
    Beat = Beat.objects.all()
    return render(request, 'beatlist.html', {'beats': beats})


from django.shortcuts import render

  # Import CartItem if you use a database-based cart


