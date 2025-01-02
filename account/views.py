from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Customer, Employee
from .serializers import UserSerializer    
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiTypes

@extend_schema(
    description="Register a new user with a specific role (customer or employee).",
    request={
        "application/json": {
            "example": {
                "user": {
                    "username": "john_doe",
                    "email": "john@example.com",
                    "password": "securepassword123"
                },
                "phone": "123456789",
                "address": "123 Main St",
                "is_active": True
            }
        }
    },
    responses={
        201: {
            "description": "User created successfully",
            "examples": {
                "application/json": {
                    "message": "User created",
                    "user": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com"
                    },
                    "profile": {
                        "phone": "123456789",
                        "address": "123 Main St",
                        "is_active": True
                    },
                    "status": 201
                }
            }
        },
        400: {
            "description": "Invalid data or role",
            "examples": {
                "application/json": {
                    "error": {
                        "username": ["This field is required."]
                    },
                    "status": 400
                }
            }
        }
    },
    parameters=[
        OpenApiParameter(
            name="role",
            description="Role of the user (customer or employee).",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH
        )
    ],
    methods=["POST"]
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request, role):
    user_data = request.data.get('user', {})
    profile_data = request.data

    user_serializer = UserSerializer(data=user_data)
    if not user_serializer.is_valid():
        return Response(
            {"error": user_serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = user_serializer.save()

    if role == 'customer':
        profile = Customer.objects.create(user=user, **profile_data)
    elif role == 'employee':
        profile = Employee.objects.create(user=user, **profile_data)
    else:
        user.delete()
        return Response(
            {"error": "Invalid role", "status": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            "message": "User created",
            "user": user_serializer.data,
            "profile": {
                "phone": profile.phone,
                "address": profile.address,
                "is_active": profile.is_active
            },
            "status": status.HTTP_201_CREATED
        },
        status=status.HTTP_201_CREATED
    )

@extend_schema(
    description="Authenticate a user and return JWT tokens.",
    request={
        "application/json": {
            "example": {
                "username": "john_doe",
                "password": "securepassword123"
            }
        }
    },
    responses={
        200: {
            "description": "Login successful",
            "examples": {
                "application/json": {
                    "message": "Login successful",
                    "user": {
                        "username": "john_doe",
                        "email": "john@example.com"
                    },
                    "tokens": {
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    },
                    "status": 200
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "examples": {
                "application/json": {
                    "error": "Invalid credentials",
                    "status": 401
                }
            }
        }
    },
    methods=["POST"]
)
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid credentials", "status": status.HTTP_401_UNAUTHORIZED},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "message": "Login successful",
            "user": {
                "username": user.username,
                "email": user.email
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            "status": status.HTTP_200_OK
        },
        status=status.HTTP_200_OK
    )