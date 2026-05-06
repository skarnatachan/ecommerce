from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    shippingaddress2user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                                related_name="user2shippingaddress")

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f'Shipping Address - {self.id}'


class Order(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    # shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    order2user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user2order")

    def __str__(self):
        return f'Order - {self.id}'


class OrderItem(models.Model):
    orderitem2order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order2orderitem", null=True, )
    orderitem2product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product2orderitem",
                                          null=True, )
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orderitem2user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name="user2orderitem")

    def __str__(self):
        return f'Order Item - {self.id}'
