from rest_framework import serializers
from .models import User, UserActivity

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_email_verified']

class UserActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'user_email', 'activity', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user_email']
