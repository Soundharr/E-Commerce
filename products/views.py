from rest_framework import generics
from django.http import JsonResponse
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


def home(request):
    return JsonResponse({"message": "Welcome to the E-Commerce API"})


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     queryset = Product.objects.filter(is_active=True).order_by('-created_at')
    #     category_name = self.request.query_params.get('category')
    #     if category_name:
    #         category = Category.objects.filter(name=category_name).first()
    #         if category:
    #             queryset = queryset.filter(category=category)
    #         else:
    #             queryset = queryset.none()
    #     return queryset
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by('-created_at')
        category_name = self.request.query_params.get('category')
        if category_name:
            category = Category.objects.filter(name=category_name).first()
            print(f"Filtering products for category: {category_name}")  # Log the category being used
            if category:
                queryset = queryset.filter(category=category)
            else:
                queryset = queryset.none()
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
