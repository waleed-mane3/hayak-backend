from rest_framework import permissions


# Get, update or delete if the client is the owner of the object ######
class ClientAccountObjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method not in permissions.SAFE_METHODS:
            return obj == request.user
#######################################################################