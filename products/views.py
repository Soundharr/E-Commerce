from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.utils.text import slugify

# List and Create Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = self.request.data.get('title')
        if title:
            slug = slugify(title)
            serializer.save(slug=slug)
        else:
            serializer.save()

# Retrieve, Update, Delete Product
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'  # So you can use slug in the URL

from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Category List
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
