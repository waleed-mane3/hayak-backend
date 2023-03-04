from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from package.models import Package





@admin.register(Package)
class PackageImportExport(ImportExportModelAdmin):
    list_display = ['id', 'name', 'price']