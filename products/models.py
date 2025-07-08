from django.db import models
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='category_images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(
        upload_to='product_images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

