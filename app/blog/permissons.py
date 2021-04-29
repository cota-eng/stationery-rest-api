from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "you must be an owner"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        ここでメンバー限定にするなら、、、
        member = Membership.objects.get(user=request.user)
        member.is_active...
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
