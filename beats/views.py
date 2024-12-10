from django.shortcuts import render
from instrumentals.models import Beat
from django.db.models import Q 
from bag.models import CartItem
from checkout.views import payment_success
 # Adjust this import based on your project structure
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from django.core.mail import send_mail
from django.contrib import messages





def index(request):
    return render(request, 'home.html')  # This will render 'home.html', which can extend 'base.html'



def contact(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Construct the subject and message
        subject = f"New Contact Form Submission from {name}"
        message_body = f"""
        You have a new message from the contact form on your website.

        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """

        try:
            # Send the email to the admin
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,  # From email (your app's email)
                ['twintwobeats@gmail.com'],  # Admin email (replace with the admin's email)
                fail_silently=False,  # Set to True if you don't want to see errors
            )
            messages.success(request, 'Your message has been sent successfully!')  # Optional success message
            return redirect('contact')  # Redirect to avoid form resubmission
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")  # Display the error (optional)

    return render(request, 'contact.html')  # Render the form if GET request

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


