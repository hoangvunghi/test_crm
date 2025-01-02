from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from base.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class ProductListView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        description="Retrieve a list of products. Anyone can view the list, but only admins can create new products.",
        responses={200: ProductSerializer(many=True)},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Products retrieved successfully",
                    "data": [
                        {
                            "id": 1,
                            "name": "Product A",
                            "price": 100.0,
                            "description": "This is Product A",
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": "2023-10-01T12:00:00Z"
                        }
                    ],
                    "status": 200
                }
            )
        ]
    )
    def get(self, request):
        """
        Lấy danh sách các Product (ai cũng có quyền xem).
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                "message": "Products retrieved successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Create a new product. Only admins have permission to create products.",
        request=ProductSerializer,
        responses={201: ProductSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "name": "Product B",
                    "price": 200.0,
                    "description": "This is Product B"
                }
            )
        ]
    )
    def post(self, request):
        """
        Tạo mới Product (chỉ admin mới có quyền).
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product created successfully",
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

class ProductDetailView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @extend_schema(
        description="Retrieve details of a specific product. Anyone can view the details, but only admins can update or delete the product.",
        responses={200: ProductSerializer},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Product retrieved successfully",
                    "data": {
                        "id": 1,
                        "name": "Product A",
                        "price": 100.0,
                        "description": "This is Product A",
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": "2023-10-01T12:00:00Z"
                    },
                    "status": 200
                }
            )
        ]
    )
    def get(self, request, pk):
        """
        Lấy thông tin chi tiết của một Product (ai cũng có quyền xem).
        """
        product = self.get_object(pk)
        if product:
            serializer = ProductSerializer(product)
            return Response(
                {
                    "message": "Product retrieved successfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Product not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Update a specific product. Only admins have permission to update products.",
        request=ProductSerializer,
        responses={200: ProductSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "name": "Updated Product A",
                    "price": 150.0,
                    "description": "This is the updated Product A"
                }
            )
        ]
    )
    def put(self, request, pk):
        """
        Cập nhật thông tin của một Product (chỉ admin mới có quyền).
        """
        product = self.get_object(pk)
        if product:
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Product updated successfully",
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
                "message": "Product not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Delete a specific product. Only admins have permission to delete products.",
        responses={204: None},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Product deleted successfully",
                    "status": 204
                }
            )
        ]
    )
    def delete(self, request, pk):
        """
        Xóa một Product (chỉ admin mới có quyền).
        """
        product = self.get_object(pk)
        if product:
            product.delete()
            return Response(
                {
                    "message": "Product deleted successfully",
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {
                "message": "Product not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )