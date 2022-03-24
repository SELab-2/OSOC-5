"""
Permission classes specific to the OSOC application.
"""
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission class that allows OSOC admins to edit a view.
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
