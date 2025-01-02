from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    """
    Chỉ admin hoặc chủ sở hữu mới có quyền thực hiện hành động.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.user

class IsAdmin(BasePermission):
    """
    Chỉ admin mới có quyền thực hiện hành động.
    """
    def has_permission(self, request, view):
        return request.user.is_staff
    
class IsAdminOrAssignedEmployee(BasePermission):
    """
    Chỉ admin hoặc nhân viên được phân công mới có quyền thực hiện hành động.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.assigned_to.user
    
class IsAdminOrReadOnly(BasePermission):
    """
    Cho phép ai cũng có quyền đọc (GET), nhưng chỉ admin mới có quyền ghi (POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        # Cho phép tất cả các phương thức GET, HEAD, OPTIONS
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Chỉ admin mới có quyền thực hiện các phương thức khác
        return request.user and request.user.is_staff