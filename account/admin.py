from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from account.models import *


@admin.register(Client)
class ClientImportExport(ImportExportModelAdmin):
    list_display = ['user', 'field', 'is_assistant']



@admin.register(Admin)
class AdminImportExport(ImportExportModelAdmin):
    list_display = ['user', 'field']


@admin.register(Scanner)
class ScannerImportExport(ImportExportModelAdmin):
    list_display = ['user']