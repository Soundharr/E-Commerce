from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    home,
    ProductListCreateView, ProductDetailView,
    CategoryListCreateView, CategoryDetailView
)

urlpatterns = [
    # Home endpoint for a welcome message or any other default behavior
    path('', home, name='home'),

    # Category Endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Product Endpoints
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]

# Serving media files during development (only when DEBUG is True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
