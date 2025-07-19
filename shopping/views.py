from rest_framework import generics
from rest_framework.views import APIView
from django.http import HttpResponse
#import pandas as pd
from io import BytesIO
from .models import Address
from .serializers import AddressSerializer

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

# class AddressExportExcelView(APIView):
    # def get(self, request):
    #     # Fetch all Address records
    #     addresses = Address.objects.all()
    #     serializer = AddressSerializer(addresses, many=True)
    #     data = serializer.data
        
    #     # Convert serialized data to DataFrame
    #     df = pd.DataFrame(data)
        
    #     # Create in-memory Excel file
    #     output = BytesIO()
    #     with pd.ExcelWriter(output, engine='openpyxl') as writer:
    #         df.to_excel(writer, index=False, sheet_name='Addresses')
        
    #     # Return response with Excel file for download
    #     response = HttpResponse(
    #         output.getvalue(),
    #         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #     )
    #     response['Content-Disposition'] = 'attachment; filename=addresses.xlsx'
        
    #     return response
