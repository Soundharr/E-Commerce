# Ecommerce/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # Includes app-level URLs
    path('shop/', include('shopping.urls')),  # Includes app-level URLs
    path('register/', include('shopping.urls')),  # Includes app-level URLs
]

# Serve media files during development (only when DEBUG is True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
