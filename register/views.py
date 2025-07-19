from django.shortcuts import render

# Create your views here.
import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailOTP, User
from django.core.mail import send_mail
from django.conf import settings


class RequestOtpView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        otp = f"{random.randint(100000, 999999)}"
        # Save or update OTP for this email
        EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp, 'created_at': timezone.now()})

        # Send OTP via email
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {otp}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = EmailOTP.objects.get(email=email, otp=otp)
        except EmailOTP.DoesNotExist:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP is expired
        if otp_record.is_expired():
            return Response({"error": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

        # OTP valid - create or get user
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.save()

        # Optionally delete OTP after verification
        otp_record.delete()

        return Response({"message": "OTP verified. User logged in."}, status=status.HTTP_200_OK)
    
from rest_framework import generics, permissions
from .models import UserActivity
from .serializers import UserActivitySerializer

class UserActivityListCreateView(generics.ListCreateAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the current logged in user as the user for the activity
        serializer.save(user=self.request.user)

