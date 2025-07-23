from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random
from .models import EmailOTP, User
from .serializers import UserSerializer
from django.core.mail import BadHeaderError
from rest_framework import generics, permissions
from .models import UserActivity  # Assuming UserActivity is in models.py of the same app
from .serializers import UserActivitySerializer 


from datetime import timedelta
from django.utils import timezone

class RequestOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP request is too frequent
        recent_otp = EmailOTP.objects.filter(
            email=email, created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()
        if recent_otp:
            return Response({"error": "You can only request an OTP every 5 minutes."}, status=status.HTTP_400_BAD_REQUEST)

        otp = f"{random.randint(100000, 999999)}"

        # Save or update OTP for this email
        EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp, 'created_at': timezone.now()})

        # Send OTP via email using the configured SMTP settings
        try:
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp}. It expires in 5 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = EmailOTP.objects.get(email=email, otp=otp)
        except EmailOTP.DoesNotExist:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.is_expired():
            return Response({"error": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.save()

        otp_record.delete()

        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            "message": "OTP verified.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user_data
        })


class UserActivityListCreateView(generics.ListCreateAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
    # Optionally log the user's IP and User-Agent
        user_activity = serializer.save(
            user=self.request.user,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
            )

