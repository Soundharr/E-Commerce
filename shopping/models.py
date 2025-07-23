from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from products.models import Product

from django.db import models
from decimal import Decimal
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.BigIntegerField()

    door_no = models.CharField(max_length=10)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()

    date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    def update_total_amount(self):
        """Updates the total amount of the order based on its related order items."""
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at purchase time

    def save(self, *args, **kwargs):
        """Calculate the price at the time of purchase and update total amount on save."""
        self.price = self.product.discount_price or self.product.price or Decimal('0.00')
        super().save(*args, **kwargs)
        self.order.update_total_amount()

    def get_total_price(self):
        """Calculates the total price of this order item."""
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in order {self.order.id}"

    @property
    def product_image_url(self):
        """Fetch the product image URL from the related Product model."""
        return self.product.image_url if self.product.image_url else "https://via.placeholder.com/150"
