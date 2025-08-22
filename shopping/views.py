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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import EnquiryForm
from .serializers import EnquiryFormSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def enquiry_list(request):
    if request.method == 'GET':
        enquiries = EnquiryForm.objects.all()
        serializer = EnquiryFormSerializer(enquiries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = EnquiryFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Enquiry submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# For admin
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Order
from .serializers import OrderSerializer

class AdminOrderCRUDView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # ⚠️ No authentication

class AdminOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # ⚠️ No authentication
