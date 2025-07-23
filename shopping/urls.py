from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('test/', views.AddressTestView.as_view(), name='address-test'),
    path('debug-auth/', views.DebugAuthView.as_view(), name='debug-auth'),
]
