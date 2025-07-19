
from django.urls import path
from .views import RequestOtpView, VerifyOtpView,UserActivityListCreateView

urlpatterns = [
    path('request-otp/', RequestOtpView.as_view(), name='request-otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('activities/', UserActivityListCreateView.as_view(), name='user-activities'),
]