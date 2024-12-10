from django import forms
from checkout.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name',
         'email', 'phone_number',
         'street_address1', 'street_address2',
         'city', 
         'postcode', 'country',
         )

    def __init__(self, *args, **kwargs):
        """
        placeholders and classes auto generated labels
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number', 
            'postcode': 'Postal Code',
            'city': 'City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2', 
            'country': 'Country',
        }


        self.fields['full_name'].widget.attrs['autofocus']= True
        for field in self.fields:
            if self.fields[field].required:
                placeholder= f'{placeholders[field]}*'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
