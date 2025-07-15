from rest_framework import serializers
from .models import Category, Product
import cloudinary.uploader

class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Added to return Cloudinary URL

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'image_url']
        read_only_fields = ['image_url']

    # def get_image_url(self, obj):
    #     # This returns the Cloudinary URL for the image
    #     if obj.image:
    #         return obj.image.url  # Cloudinary URL will automatically be generated
    #     return None
    def create(self, validated_data):
        image = validated_data.pop('image')
        # Upload image file to Cloudinary
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result.get('secure_url')
        category = Category.objects.create(image_url=image_url, **validated_data)
        return category


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
            return obj.image.url  # Cloudinary URL will automatically be generated
        return None
