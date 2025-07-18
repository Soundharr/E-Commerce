from rest_framework import serializers
from .models import Address
from products.models import Product

class AddressSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'door_no',
            'area',
            'city',
            'state',
            'pincode',
            'product',
            'product_title',
            'quantity',
            'total_amount',
        ]
        read_only_fields = ['total_amount']  # it's auto-calculated
