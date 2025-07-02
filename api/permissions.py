from rest_framework.permissions import BasePermission

class IsOpsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'client'
