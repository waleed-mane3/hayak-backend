from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_type', 'first_sign_in',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'mobile', 'image',)}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'mobile', 'user_type', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'first_name', 'last_name', 'email', 'mobile', 'user_type', 'is_active', 'date_joined')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'mobile',)
    list_filter = ['is_active', 'user_type']
    ordering = ('-id',)
    readonly_fields = ('date_joined', 'last_login',)
