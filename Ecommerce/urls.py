from django.contrib import admin
from django.urls import path, include
from products.views import home  # import home view here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # root URL served directly by home view
    path('products/', include("products.urls")),
]