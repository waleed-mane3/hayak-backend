from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from scan.models import Scan
# from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter



# class CheckinResource(resources.ModelResource):
#     class Meta:
#         model = Checkin
#         fields = ('invitation__first_name', 'invitation__last_name', 'invitation__email', 'date', 'time',)
#         export_order = ('invitation__first_name', 'invitation__last_name', 'invitation__email', 'date', 'time',)

@admin.register(Scan)
class ScanImportExport(ImportExportModelAdmin):
    list_display = ['id', 'event', 'scanned_by', 'invitation', 'date', 'time']
    # list_filter = (
    #     ('date', DateRangeFilter), 
    #     # ('updated_at', DateTimeRangeFilter),
    # )
    # resource_class = CheckinResource