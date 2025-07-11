from rest_framework import generics
from django.http import JsonResponse
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Simple home endpoint
def home(request):
    return JsonResponse({"message": "Welcome to the E-Commerce API"})


# Product views

class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: List all active products, optionally filtered by category name.
    POST: Create a new product with image upload.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by('-created_at')
        category_name = self.request.query_params.get('category')

        if category_name:
            category = Category.objects.filter(name=category_name).first()
            if category:
                queryset = queryset.filter(category=category)
            else:
                # No category found, return empty queryset
                queryset = queryset.none()

        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve product by ID.
    PUT/PATCH: Update product (including image).
    DELETE: Delete product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# Category views

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List all categories.
    POST: Create a new category (with optional image).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a category by PK.
    PUT/PATCH: Update category.
    DELETE: Delete category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


# Optional: Category list-only view without create

class CategoryListView(generics.ListAPIView):
    """
    GET: List all categories (read-only).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
