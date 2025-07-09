# urls.py in your app (products/urls.py)

from django.urls import path
from . import views  # Import views here

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
]
