from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Task
from .serializers import TaskSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from base.permissions import IsAdminOrAssignedEmployee, IsAdmin
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class TaskListView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdminOrAssignedEmployee]

    @extend_schema(
        description="Retrieve a list of tasks. Admins can see all tasks, while employees can only see tasks assigned to them.",
        responses={200: TaskSerializer(many=True)},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Tasks retrieved successfully",
                    "data": [
                        {
                            "id": 1,
                            "title": "Fix bug",
                            "description": "Fix the bug in the login module",
                            "status": "todo",
                            "assigned_to": 1,
                            "due_date": "2023-12-31",
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
        Lấy danh sách các Task.
        """
        if request.user.is_staff:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to__user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(
            {
                "message": "Tasks retrieved successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Create a new task. Only admins have permission to create tasks.",
        request=TaskSerializer,
        responses={201: TaskSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "title": "Fix bug",
                    "description": "Fix the bug in the login module",
                    "status": "todo",
                    "assigned_to": 1,
                    "due_date": "2023-12-31"
                }
            )
        ]
    )
    def post(self, request):
        """
        Tạo mới Task (chỉ admin mới có quyền).
        """
        if not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to create a task", "status": status.HTTP_403_FORBIDDEN},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Task created successfully",
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

class TaskDetailView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAdminOrAssignedEmployee]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    @extend_schema(
        description="Retrieve details of a specific task.",
        responses={200: TaskSerializer},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Task retrieved successfully",
                    "data": {
                        "id": 1,
                        "title": "Fix bug",
                        "description": "Fix the bug in the login module",
                        "status": "todo",
                        "assigned_to": 1,
                        "due_date": "2023-12-31",
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
        Lấy thông tin chi tiết của một Task.
        """
        task = self.get_object(pk)
        if task:
            serializer = TaskSerializer(task)
            return Response(
                {
                    "message": "Task retrieved successfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Task not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Update a specific task. Only admins or assigned employees have permission to update tasks.",
        request=TaskSerializer,
        responses={200: TaskSerializer},
        examples=[
            OpenApiExample(
                name="Example Request",
                value={
                    "title": "Fix bug",
                    "description": "Fix the bug in the login module",
                    "status": "in_progress"
                }
            )
        ]
    )
    def put(self, request, pk):
        """
        Cập nhật thông tin của một Task (chỉ admin hoặc nhân viên được phân công mới có quyền).
        """
        task = self.get_object(pk)
        if task:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Task updated successfully",
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
                "message": "Task not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        description="Delete a specific task. Only admins have permission to delete tasks.",
        responses={204: None},
        examples=[
            OpenApiExample(
                name="Example Response",
                value={
                    "message": "Task deleted successfully",
                    "status": 204
                }
            )
        ]
    )
    def delete(self, request, pk):
        """
        Xóa một Task (chỉ admin mới có quyền).
        """
        if not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to delete a task", "status": status.HTTP_403_FORBIDDEN},
                status=status.HTTP_403_FORBIDDEN
            )
        task = self.get_object(pk)
        if task:
            task.delete()
            return Response(
                {
                    "message": "Task deleted successfully",
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {
                "message": "Task not found",
                "status": status.HTTP_404_NOT_FOUND
            },
            status=status.HTTP_404_NOT_FOUND
        )