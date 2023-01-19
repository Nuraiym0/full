from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Post

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
        if isinstance(obj, Post):
            return request.user == obj.title_of_restourant.author
        return request.user == obj.author
    
class IsAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
    