from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Customer
from rest_framework.authentication import BasicAuthentication
from .serializers import CustomerSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.permissions import IsAdmin, IsAdminOrOwner
from drf_spectacular.utils import extend_schema, OpenApiExample

class CustomerListView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
        description="Retrieve a list of active customers. Only admins have permission to view the list.",
        responses={200: CustomerSerializer(many=True)},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Customers retrieved successfully",
                    "data": [
                        {
                            "id": 1,
                            "user": 1,
                            "phone": "123456789",
                            "address": "123 Main St",
                            "is_active": True
                        }
                    ],
                    "status": 200
                }
            )
        ]
    )
    def get(self, request):
        """
        Lấy danh sách các Customer đang hoạt động (chỉ admin mới có quyền).
        """
        customers = Customer.objects.filter(is_active=True)
        serializer = CustomerSerializer(customers, many=True)
        return Response(
            {
                "message": "Customers retrieved successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Create a new customer. Only admins have permission to create customers.",
        request=CustomerSerializer,
        responses={201: CustomerSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "user": 2,
                    "phone": "987654321",
                    "address": "456 Elm St",
                    "is_active": True
                }
            )
        ]
    )
    def post(self, request):
        """
        Tạo mới Customer (chỉ admin mới có quyền).
        """
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Customer created successfully",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Invalid data",
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CustomerDetailView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk, is_active=True)
        except Customer.DoesNotExist:
            return None

    @extend_schema(
        description="Retrieve details of a specific customer. Only admins or the owner have permission to view the details.",
        responses={200: CustomerSerializer},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Customer retrieved successfully",
                    "data": {
                        "id": 1,
                        "user": 1,
                        "phone": "123456789",
                        "address": "123 Main St",
                        "is_active": True
                    },
                    "status": 200
                }
            )
        ]
    )
    def get(self, request, pk):
        """
        Lấy thông tin chi tiết của một Customer (chỉ admin hoặc chủ sở hữu mới có quyền).
        """
        customer = self.get_object(pk)
        if customer:
            serializer = CustomerSerializer(customer)
            return Response(
                {
                    "message": "Customer retrieved successfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Customer not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Update a specific customer. Only admins or the owner have permission to update the customer.",
        request=CustomerSerializer,
        responses={200: CustomerSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "phone": "987654321",
                    "address": "456 Elm St"
                }
            )
        ]
    )
    def put(self, request, pk):
        """
        Cập nhật thông tin của một Customer (chỉ admin hoặc chủ sở hữu mới có quyền).
        """
        customer = self.get_object(pk)
        if customer:
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Customer updated successfully",
                        "data": serializer.data,
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    "message": "Invalid data",
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "message": "Customer not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Soft delete a specific customer. Only admins or the owner have permission to delete the customer.",
        responses={204: None},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Customer deleted successfully",
                    "status": 204
                }
            )
        ]
    )
    def delete(self, request, pk):
        """
        Xóa mềm một Customer (chỉ admin hoặc chủ sở hữu mới có quyền).
        """
        customer = self.get_object(pk)
        if customer:
            customer.soft_delete()
            return Response(
                {
                    "message": "Customer deleted successfully",
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {
                "message": "Customer not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )