from django.urls import path
from . import views

urlpatterns = [
    path('address/', views.AddressListCreateView.as_view(), name='address-list-create'),
    path('address/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
    #path('addresses/export/', AddressExportExcelView.as_view(), name='address-export-excel'),
]
