from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrIsAdminOrReadOnly(BasePermission):
    """Пермишен пускает только Автора или Администратора. Для остальных доступ
    только на чтение.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff  # Если админ не может создавать, закомментируй
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )




from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Product

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, Product):
            return request.user == obj.course.author
        return request.user == obj.author
    