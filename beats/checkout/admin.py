# checkout/admin.py
from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    fields = ('product', 'quantity', 'lineitem_total')
    extra = 0  # Avoid extra blank rows in the inline

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineItemAdminInline]
    readonly_fields = ('order_number', 'date', 'order_total', 'grand_total')
    fields = ('order_number', 'date', 'full_name', 'email', 'phone_number',
              'country', 'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'order_total', 'grand_total')
    list_display = ('order_number', 'date', 'full_name', 'email', 'order_total', 'grand_total', 'country')
    ordering = ('-date',)
    search_fields = ('order_number', 'full_name', 'email')

# Register the Order model with the admin interface
admin.site.register(Order, OrderAdmin)

