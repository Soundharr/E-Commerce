from rest_framework import serializers
from .models import Product, Category

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'discount_price', 'description',
            'stock', 'is_active', 'image', 'image_url', 'created_at', 'updated_at',
            'category', 'category_id'
        ]

    def get_image_url(self, obj):
        # Ensure we return the full URL for the image (MEDIA_URL + image path)
        if obj.image:
            return obj.image.url
        return None
