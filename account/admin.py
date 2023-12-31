from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from account.models import Client, Admin


@admin.register(Client)
class ClientImportExport(ImportExportModelAdmin):
    list_display = ['user', 'field', 'is_assistant']


@admin.register(Admin)
class AdminImportExport(ImportExportModelAdmin):
    list_display = ['user', 'field']

















# @admin.register(Scanner)
# class ScannerImportExport(ImportExportModelAdmin):
#     list_display = ['user']


# class RegularAdmin(admin.ModelAdmin):
#     model = Regular

#     list_display = ['user']


# class DataEntryAdmin(admin.ModelAdmin):
#     model = DataEntry
#     list_display = ['user']


# admin.site.register(Regular, RegularAdmin)
# admin.site.register(DataEntry, DataEntryAdmin)


