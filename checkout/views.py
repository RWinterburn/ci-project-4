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
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)
stripe_public_key = settings.STRIPE_PUBLIC_KEY

print('SPK: ', stripe_public_key)

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        order_number = request.session.get('order_number')
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'order_number': order_number
        })
        return HttpResponse(status=200)
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error in cache_checkout_data: {e}")
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=f"Error: {e}", status=400)


def checkout(request):
    stripe_public_key=settings.STRIPE_PUBLIC_KEY
    stripe_secret_key=settings.STRIPE_SECRET_KEY

    print("Stripe Public Key:", stripe_public_key)

    print('REQUEST: ', request)

    if request.method == 'POST':
        print('WH : ', request.POST.get('client_secret').split('_secret')[0])
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, quantity in bag.items():
                try:
                    beat = Beat.objects.get(id=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        beat=beat,
                        quantity=quantity,
                    )
                except Beat.DoesNotExist:
                    messages.error(request, (
                        "One of the items in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('payment_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    else:
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
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.full_name,
                    'email': profile.email,
                    'phone_number': profile.phone_number,
                    'country': profile.country,
                    'postcode': profile.postal_code,
                    'city': profile.city,
                    'street_address1': profile.street_address1,
                    'street_address2': profile.street_address2,
                    
                })
            except Profile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def payment_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

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

    # Retrieve all line items for the order
    purchased_items = OrderLineItem.objects.filter(order=order)

    # Construct download links for purchased beats
    download_links = []
    for item in purchased_items:
        if item.beat and item.beat.audio_file:
            download_links.append({
                'title': item.beat.title,
                'url': request.build_absolute_uri(item.beat.audio_file.url),
            })

    # Email confirmation with download links
    subject = f"Order Confirmation - {order_number}"
    message = (
        f"Dear {order.full_name},\n\n"
        f"Thank you for your purchase! Your order has been successfully processed.\n\n"
        f"Order Number: {order_number}\n"
        f"Total: ${order.grand_total}\n\n"
        f"You can download your purchased beats using the links below:\n"
    )
    for link in download_links:
        message += f"- {link['title']}: {link['url']}\n"

    message += "\nBest regards,\nThe Team"

    recipient = order.email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )

    # Success message for the user
    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. A confirmation email has been sent to {order.email}.'
    )

    # Clear the shopping bag
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/payment_success.html'
    context = {
        'order': order,
        'purchased_items': purchased_items,
          # Pass links for displaying on the success page (optional)
    }

    return render(request, template, context)