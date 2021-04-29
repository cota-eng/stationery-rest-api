from rest_framework import permissions


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    """
    IsAuthenticated is that user can see info about profile
    and personA can change(not safe method) PersonB profile
    this is not allowed, so this permission is needed
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.profile.id
