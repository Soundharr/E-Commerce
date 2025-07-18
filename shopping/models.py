from django.db import models
from django.utils import timezone
from decimal import Decimal
from products.models import Product


class Address(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    mobile = models.BigIntegerField()
    door_no = models.CharField(max_length=10)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='addresses')
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        price = self.product.discount_price or self.product.price or Decimal('0.00')
        self.total_amount = price * self.quantity
        super().save(*args, **kwargs)
