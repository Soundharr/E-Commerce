from django.urls import path
from . import views
from .views import enquiry_list

urlpatterns = [
    
]


urlpatterns = [
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('test/', views.AddressTestView.as_view(), name='address-test'),
    path('debug-auth/', views.DebugAuthView.as_view(), name='debug-auth'),
    path('enquiry/', enquiry_list, name='enquiry-list'),
    path('admin/orders/', views.AdminOrderCRUDView.as_view(), name='admin-order-crud'),
    path('admin/orders/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),


]
