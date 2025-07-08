from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListView, CategoryListCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Use either CategoryListView or CategoryListCreateView for 'categories/'
    # Assuming CategoryListCreateView handles both GET and POST:
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
