from rest_framework import serializers
from .models import Category, Product
import cloudinary.uploader


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'image_url']
        read_only_fields = ['image_url']

    def create(self, validated_data):
        image = validated_data.pop('image')
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result.get('secure_url')
        return Category.objects.create(image_url=image_url, **validated_data)
    

    def get_image(self, obj):
        # Assuming 'image_url' is the field in the model, convert to a proper full URL
        image_url = obj.image_url
        if image_url.startswith("http"):
            return image_url  # If it's already a full URL, return it
        return f"https://e-commerce-oagd.onrender.com{image_url}" 


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'discount_price', 'description', 'stock', 'is_active',
            'image', 'image_url', 'created_at', 'updated_at', 'category', 'category_id'
        ]
        read_only_fields = ['image_url', 'created_at', 'updated_at']

    def create(self, validated_data):
        image = validated_data.pop('image')
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result.get('secure_url')
        validated_data['image_url'] = image_url
        return Product.objects.create(**validated_data)

    def get_image(self, obj):
        # Assuming 'image_url' is the field in the model, convert to a proper full URL
        image_url = obj.image_url
        if image_url.startswith("http"):
            return image_url  # If it's already a full URL, return it
        return f"https://e-commerce-oagd.onrender.com{image_url}" 