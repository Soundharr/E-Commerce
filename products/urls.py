from django.urls import path
from .views import (
    home,
    ProductListCreateView, ProductDetailView,
    CategoryListCreateView, CategoryDetailView
)

urlpatterns = [
    path('', home, name='home'),  # 👈 This is the root of the app
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]
