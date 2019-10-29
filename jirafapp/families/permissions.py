"""Families permissions."""

# Django Rest Framework
from rest_framework.permissions import BasePermission


class IsParent(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check thath user is the kid's parent"""
        return request.user == obj.parent