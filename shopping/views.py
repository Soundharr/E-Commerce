from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure user only accesses their own orders
        return Order.objects.filter(user=self.request.user)

class AddressTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        user = request.user
        return Response({
            "auth_header": auth_header,
            "user": str(user),
            "user_id": user.id if user.is_authenticated else None,
        })

class DebugAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": str(request.user),
            "auth": str(request.auth)
        })
