

// Remove extra characters and retrieve keys from the script elements
var stripe_public_key = document.getElementById('id_stripe_public_key').textContent.trim();
var client_secret = document.getElementById('id_client_secret').textContent.trim();

// Initialize Stripe
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();
var card = elements.create('card');
card.mount('#card-element');
