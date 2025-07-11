from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Added to return Cloudinary URL

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'image_url']

    def get_image_url(self, obj):
        # This returns the Cloudinary URL for the image
        if obj.image:
            return obj.image.url
        return None
from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    image_url = serializers.SerializerMethodField()  # Added to return Cloudinary URL

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'discount_price', 'description', 'stock', 'is_active',
            'image', 'image_url', 'created_at', 'updated_at', 'category', 'category_id'
        ]

    def get_image_url(self, obj):
        # This returns the Cloudinary URL for the image
        if obj.image:
            return obj.image.url
        return None
