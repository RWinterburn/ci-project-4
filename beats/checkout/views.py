from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import OrderForm  # Ensure this form is defined correctly
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})

    # If the bag is empty, redirect to the 'view_cart' page with an error message
    if not bag:
        messages.error(request, 'There is nothing in your bag')
        return redirect(reverse('view_cart'))  # Redirect to 'view_cart' page

    # Create the order form instance
    order_form = OrderForm()

    # Define the template path
    template = 'checkout/checkout.html'
    context = { 
        'order_form': order_form,
    }

    # Render the checkout template
    return render(request, template, context)

