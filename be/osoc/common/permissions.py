from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit the view
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS or view.action in ['suggest_student', 'remove_student']:
            return True

        # Write permissions are only allowed to the admin
        return request.user.is_admin
