from rest_framework import generics, mixins, permissions

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    """
    IsAuthenticated is user can see info about profile
    personA can change PersonB profile
    this is not allowed, so this permission is needed
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
