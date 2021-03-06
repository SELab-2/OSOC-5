"""
Permission classes specific to the OSOC application.
"""
from rest_framework import permissions


class IsAdminOrSafe(permissions.BasePermission):
    """
    Custom permission class that allows OSOC admins to edit a view (POST, PUT, PATCH and DELETE).
    this allows everyone to still retrieve information (GET)
    """

    def has_permission(self, request, view):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admin
        return request.user.is_admin


class IsAdmin(permissions.BasePermission):
    """
    Custom permission class that allows OSOC admins to acces a view (POST, PUT, PATCH, DELETE and GET).
    """

    def has_permission(self, request, view):
        return request.user.is_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission that allows users to edit their own data
    """

    def has_permission(self, request, view):

        # restrict list view to admins only
        if view.action == 'list':
            return request.user.is_admin

        # else check object permission
        return True

    def has_object_permission(self, request, view, obj):

        # admins have all permissions
        # Write permissions are only allowed to the owner of the data
        return request.user.is_admin or request.user==obj


class IsActive(permissions.BasePermission):
    """
    Custom permission class that checks if the current user is active
    """

    def has_permission(self, request, view):
        return request.user.is_active
