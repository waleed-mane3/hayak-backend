
from rest_framework import permissions
from django.conf import settings


class UserTypeAccessAdminOrClient(permissions.BasePermission):

    """Permissions (USER either ADMIN or CLIENT)"""


    ### USER either ADMIN OR CLIENT ###
    message = 'Account type is not permitted to preform this request'

    def has_permission(self, request, view):
        if request.user.user_type != settings.SCANNER:
             return True
             
        return False