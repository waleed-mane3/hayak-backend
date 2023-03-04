from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin


from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type', 'image',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'mobile','first_sign_in')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type','image'),
        }),
    )
    list_display = ('id', 'email', 'mobile', 'first_name', 'last_name', 'user_type')
    search_fields = ('email', 'mobile','first_name', 'last_name')
    ordering = ('id',)