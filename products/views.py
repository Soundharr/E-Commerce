from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Q
from django.http import JsonResponse

# Home Endpoint - Simple welcome message
def home(request):
    return JsonResponse({"message": "Welcome to the E-Commerce API"})

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    """
    View to list all products and create a new product.
    This view filters products based on the 'category' query parameter.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally filters the products by category based on the query parameter.
        """
        queryset = Product.objects.filter(is_active=True).order_by('-created_at')
        category_name = self.request.query_params.get('category', None)

        if category_name:
            # Filter products by category name
            category = Category.objects.filter(name=category_name).first()
            if category:
                queryset = queryset.filter(category=category)

        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  # Use 'id' instead of slug

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    View to list all categories and create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'  # You can use 'slug' or 'name' as well

# Category List Only View
class CategoryListView(generics.ListAPIView):
    """
    View to list all categories (without create option).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
