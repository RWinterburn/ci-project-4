import stripe
import json
from django.conf import settings, os
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from instrumentals.models import Beat
from profiles.models import Profile
from profiles.forms import ProfileForm
from bag.context_processors import cart_items
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)
stripe_public_key = settings.STRIPE_PUBLIC_KEY

print('SPK: ', stripe_public_key)

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'order_number': request.POST.get('order_number')
        })
        return HttpResponse(status=200)
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error in cache_checkout_data: {e}")
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=f"Error: {e}", status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # Save the order object with commit=False so we can modify it before saving
            order = order_form.save(commit=False)
            pid = extract_pid(request.POST.get('client_secret'))
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            
            # Save the order to generate the order_number
            order.save()
            
            order_number = order.order_number  # Now we can access the order_number

            # Process line items in the cart
            for item_id, quantity in bag.items():
                try:
                    beat = Beat.objects.get(id=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        beat=beat,
                        quantity=quantity,
                    )
                except Beat.DoesNotExist:
                    messages.error(request, "One of the items in your bag wasn't found. Please call us for assistance!")
                    order.delete()  # Clean up the partially created order
                    return redirect(reverse('view_bag'))

            # Now create the PaymentIntent with the saved order details
            stripe.api_key = stripe_secret_key
            stripe_total = round(current_bag['total_price'] * 100)  # Ensure this total is calculated properly
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency='gbp',
                metadata={
                    'cart_items': json.dumps(bag),
                    'order_number': order_number  # Use the order_number after the order is saved
                }
            )

            # Save user info if needed
            request.session['save_info'] = 'save-info' in request.POST

            # Redirect to the payment success page
            return redirect(reverse('payment_success', args=[order.order_number]))
        else:
            # If the form is invalid, show the error messages
            messages.error(request, 'There was an error with your form. Please double check your information.')
            logger.error(f"Order form errors: {order_form.errors}")
    else:
        # Handle GET request when displaying the checkout page
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('beats'))

        current_bag = cart_items(request)
        total = current_bag['total_price']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='gbp',
            metadata={
                'cart_items': json.dumps(bag),
                # The order number can only be accessed after the order is saved
            }
        )





def payment_success(request, order_number):
    # Retrieve the order, or raise 404 if not found
    order = get_object_or_404(Order, order_number=order_number)

    # Get save_info from session (for saving profile info)
    save_info = request.session.get('save_info')

    # If the user is authenticated, associate the order with the user's profile
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            order.user_profile = profile
            order.save()

            # If the user wants to save their information, update their profile
            if save_info:
                profile_data = {
                    'phone_number': order.phone_number,
                    'email': profile.email,
                    'country': order.country,
                    'postcode': order.postcode,
                    'city': order.city,
                    'street_address1': order.street_address1,
                    'street_address2': order.street_address2,
                }
                profile_form = ProfileForm(profile_data, instance=profile)
                if profile_form.is_valid():
                    profile_form.save()

        except Profile.DoesNotExist:
            messages.error(request, "Profile not found. Please update your profile details.")

    # Display success message
    messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    # Retrieve purchased items related to this order
    purchased_items = OrderLineItem.objects.filter(order=order)

    # Clear the session's bag after purchase
    if 'bag' in request.session:
        del request.session['bag']

    # Send an email confirmation (optional)
    try:
        send_mail(
            f'Order Confirmation - {order_number}',
            f'Thank you for your purchase! Your order number is {order_number}.',
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")  # Handle email sending errors

    # Render the success page with order details
    template = 'checkout/payment_success.html'
    context = {
        'order': order,
        'purchased_items': purchased_items,
    }

    return render(request, template, context)
