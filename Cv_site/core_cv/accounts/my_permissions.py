from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or not request.user.is_tenant() or request.user.is_superuser


class IsCommettee(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_tenant()


class ObjOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    for message app use
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet. or admin
        return obj.author == request.user or not request.user.is_tenant() or request.user.is_superuser


class CommentAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or not request.user.is_tenant() or request.user.is_superuser
