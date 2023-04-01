from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from settings.models import *


@admin.register(General)
class GeneralImportExport(ImportExportModelAdmin):
    list_display = ['event', 'registration', 'language']

@admin.register(StaffEventSetting)
class StaffSettingImportExport(ImportExportModelAdmin):
    list_display = ['event']


@admin.register(EventSetting)
class StaffSettingImportExport(ImportExportModelAdmin):
    list_display = ['event']

@admin.register(TicketType)
class StaffSettingImportExport(ImportExportModelAdmin):
    list_display = ['name']

@admin.register(Zones)
class StaffSettingImportExport(ImportExportModelAdmin):
    list_display = ['name']