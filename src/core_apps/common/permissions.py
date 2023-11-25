""" Custom permissions """

from rest_framework import permissions


class IsAdminToPutPatchOrDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return bool(request.user and request.user.is_staff)
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_staff):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or obj.owner == request.user
