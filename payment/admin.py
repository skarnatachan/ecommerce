from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'address1', 'city']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'amount_paid', 'order_date']


# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['orderitem2order__full_name','orderitem2product', 'quantity']


admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
