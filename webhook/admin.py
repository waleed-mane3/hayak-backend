from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import AcmeWebhookMessage


@admin.register(AcmeWebhookMessage)
class AcmeImportExport(ImportExportModelAdmin):
    list_display = ['id', 'payload']