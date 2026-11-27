from django.core.signals import request_started
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        if obj.is_public and request.method in permissions.SAFE_METHODS:
            return True

        return False
