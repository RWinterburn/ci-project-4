from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import OrderForm  # Ensure this form is defined correctly
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import OrderForm

from instrumentals.models import Beat

def checkout(request):
    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})

    # If the bag is empty, redirect to the 'view_cart' page with an error message
    if not bag:
        messages.error(request, 'There is nothing in your bag')
        return redirect(reverse('view_cart'))  # Redirect to 'view_cart' page

    # Calculate the total price of all the items in the cart
    grand_total = 0
    for beat_id, quantity in bag.items():
        beat = Beat.objects.get(id=beat_id)  # Get the beat object using the ID from the session
        grand_total += beat.price * quantity  # Add the total price of each beat to grand_total

    # Create the order form instance
    order_form = OrderForm()

    # Define the template path and context
    template = 'checkout/checkout.html'
    context = { 
        'order_form': order_form,
        'grand_total': grand_total,
        'stripe_public_key': 'pk_test_51QMs27DNIGFfmTD0aPcOZsVCdJx6Kj1KULYcavy6fNtNPR1qGTyj9HfMxsvI8XbAA8BeNwSRAwL4D12C9u52QglN00a7ewNLwy',
        'client_secret_key': 'sk_test_51QMs27DNIGFfmTD0v0vo69HOYrfNrITILmrjDxgz5lRC7engEAU5bUx66QUJEKnzUrkzSuWFqGHZLPe4sAlnPG2x00maBEatWw',  # Pass the grand_total to the template
    }

    # Render the checkout template
    return render(request, template, context)


