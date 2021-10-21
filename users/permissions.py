from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission for Ownership of object
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.customer == request.user


class IsAdminOrOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to be owner or have admin access
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_admin or obj.customer == request.user
