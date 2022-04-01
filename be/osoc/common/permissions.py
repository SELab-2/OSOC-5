"""
Permission classes specific to the OSOC application.
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission class that allows OSOC admins to edit a view (PUT, POST and DELETE).
    """

    def has_permission(self, request, view):
        """
        Check if the current user can complete the request;

        Coaches that are not admins have some writing permissions:
         - Suggesting a student to a project
         - Removing their own suggestion from a project
        """

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS or view.action in ['suggest_student', 'remove_student']:
            return True

        # Write permissions are only allowed to the admin
        return request.user.is_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission that allows users to edit their own data, EXCEPT their admin status
    """

    def has_permission(self, request, view):

        # restrict list view to admins only
        if view.action == 'list':
            return request.user.is_admin

        # else check object permission
        return True

    def has_object_permission(self, request, view, object):

        # admins have all permissions
        if request.user.is_admin:
            return True

        # coaches are not allowed to change their admin status
        if view.action in ['make_admin', 'remove_admin']:
            return False

        # Write permissions are only allowed to the owner of the data
        return request.user == object
