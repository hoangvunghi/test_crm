from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Employee
from .serializers import EmployeeSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.permissions import IsAdmin, IsAdminOrOwner
from drf_spectacular.utils import extend_schema, OpenApiExample

class EmployeeListView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
        description="Retrieve a list of active employees. Only admins have permission to view the list.",
        responses={200: EmployeeSerializer(many=True)},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Employees retrieved successfully",
                    "data": [
                        {
                            "id": 1,
                            "user": 1,
                            "phone": "123456789",
                            "address": "123 Main St",
                            "position": "Developer",
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
        Lấy danh sách các Employee đang hoạt động (chỉ admin mới có quyền).
        """
        employees = Employee.objects.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(
            {
                "message": "Employees retrieved successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Create a new employee. Only admins have permission to create employees.",
        request=EmployeeSerializer,
        responses={201: EmployeeSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "user": 2,
                    "phone": "987654321",
                    "address": "456 Elm St",
                    "position": "Designer",
                    "is_active": True
                }
            )
        ]
    )
    def post(self, request):
        """
        Tạo mới Employee (chỉ admin mới có quyền).
        """
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Employee created successfully",
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

class EmployeeDetailView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk, is_active=True)
        except Employee.DoesNotExist:
            return None

    @extend_schema(
        description="Retrieve details of a specific employee. Only admins or the owner have permission to view the details.",
        responses={200: EmployeeSerializer},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Employee retrieved successfully",
                    "data": {
                        "id": 1,
                        "user": 1,
                        "phone": "123456789",
                        "address": "123 Main St",
                        "position": "Developer",
                        "is_active": True
                    },
                    "status": 200
                }
            )
        ]
    )
    def get(self, request, pk):
        """
        Lấy thông tin chi tiết của một Employee (chỉ admin hoặc chủ sở hữu mới có quyền).
        """
        employee = self.get_object(pk)
        if employee:
            serializer = EmployeeSerializer(employee)
            return Response(
                {
                    "message": "Employee retrieved successfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Employee not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Update a specific employee. Only admins or the owner have permission to update the employee.",
        request=EmployeeSerializer,
        responses={200: EmployeeSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "phone": "987654321",
                    "address": "456 Elm St",
                    "position": "Senior Developer"
                }
            )
        ]
    )
    def put(self, request, pk):
        """
        Cập nhật thông tin của một Employee (chỉ admin hoặc chủ sở hữu mới có quyền).
        """
        employee = self.get_object(pk)
        if employee:
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Employee updated successfully",
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
                "message": "Employee not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Soft delete a specific employee. Only admins or the owner have permission to delete the employee.",
        responses={204: None},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Employee deleted successfully",
                    "status": 204
                }
            )
        ]
    )
    def delete(self, request, pk):
        """
        Xóa mềm một Employee (chỉ admin hoặc chủ sở hữu mới có quyền).
        """
        employee = self.get_object(pk)
        if employee:
            employee.soft_delete()
            return Response(
                {
                    "message": "Employee deleted successfully",
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {
                "message": "Employee not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )