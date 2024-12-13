from django.shortcuts import render, redirect
from instrumentals.models import Beat
from django.db.models import Q 
from bag.models import CartItem
from checkout.views import payment_success
from django.conf import settings
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from django.core.mail import send_mail
from django.contrib import messages


def index(request):
    return render(request, 'home.html')  







def contact(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')


        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
            return redirect('contact')


        subject = f"New Contact Form Submission from {name}"
        message_body = f"""
        You have a new message from the contact form on your website.

        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """

        try:

            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL, 
                ['twintwobeats@gmail.com'], 
                fail_silently=False, 
            )
            messages.success(request, 'Your message has been sent successfully!')  
            return redirect('contact')  
        except Exception as e:
            messages.error(request, f"An error occurred: {e}") 
    return render(request, 'contact.html')


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.beat.price * item.quantity
    return render(request, 'instrumentals/cart.html', {'cart_items': cart_items})


def search(request):
    query = request.GET.get('q', '')  
    beats = Beat.objects.filter(
        Q(title__icontains=query) |
        Q(producer__icontains=query) |
        Q(description__icontains=query) |
        Q(price__icontains=query)
    ) if query else Beat.objects.all() 
    return render(request, 'search.html', {'beats': beats, 'query': query})


def beatlist(request):
    Beat = Beat.objects.all()
    return render(request, 'beatlist.html', {'beats': beats})


from django.shortcuts import render



