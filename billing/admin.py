from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from billing.models import *


@admin.register(Cards)
class CardsImportExport(ImportExportModelAdmin):
    list_display = ['user', 'name', 'number']


@admin.register(PaymentMethod)
class PaymentMethodImportExport(ImportExportModelAdmin):
    list_display = ['name']

@admin.register(Transactions)
class TransactionsImportExport(ImportExportModelAdmin):
    list_display = ['user', 'invoice_id', 'status']

# Register your models here.
