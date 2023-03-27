from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from settings.models import *


@admin.register(General)
class GeneralImportExport(ImportExportModelAdmin):
    list_display = ['event', 'registration', 'language']
