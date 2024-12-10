# checkout/admin.py
from django.contrib import admin
from .models import Order, OrderLineItem  # Import your models

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    fields = ('beat', 'quantity', 'lineitem_total')
    extra = 0  # Avoid showing extra empty rows

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'order_total', 'grand_total', 'stripe_payment_id','stripe_payment_status','stripe_metadata')
    fields = ('order_number', 'date', 'full_name', 'email', 'phone_number',
              'country', 'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'order_total', 'grand_total',)
    list_display = ('order_number', 'date', 'full_name', 'email', 'order_total', 'grand_total', 'country')
    ordering = ('-date',)
    search_fields = ('order_number', 'full_name', 'email')

    def get_readonly_fields(self, request, obj=None):
        # Make sure totals are always readonly
        if obj:
            obj.update_total()  # Ensure total is up-to-date when viewing the order
        return self.readonly_fields

admin.site.register(Order, OrderAdmin)





