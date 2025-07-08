from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListView, CategoryListCreateView,CategoryDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Use either CategoryListView or CategoryListCreateView for 'categories/'
    # Assuming CategoryListCreateView handles both GET and POST:
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
