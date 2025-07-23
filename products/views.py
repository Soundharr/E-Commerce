from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


# Health check endpoint or basic welcome route
def home(request):
    return JsonResponse({"message": "Welcome to the E-Commerce API"})


# Product listing and creation (admin POST, public GET)
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Allows anyone to view products; restrict POST if needed

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by('-created_at')

        category_name = self.request.query_params.get('category')
        if category_name:
            # Case-insensitive match to improve UX
            category = Category.objects.filter(name__iexact=category_name).first()
            if category:
                queryset = queryset.filter(category=category)
            else:
                queryset = Product.objects.none()  # No match found

        return queryset


# Single product detail (GET/PUT/DELETE)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Adjust to IsAuthenticated if needed
    lookup_field = 'id'


# All categories (GET and POST)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # You can restrict creation to admin users


# Single category detail (GET/PUT/DELETE)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


# Just list categories (GET only)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
