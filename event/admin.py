from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from event.models import EventType, InvitationStatus, Event, Invitation, Title, Rank, Order
# from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter



# class CheckinResource(resources.ModelResource):
#     class Meta:
#         model = Checkin
#         fields = ('invitation__first_name', 'invitation__last_name', 'invitation__email', 'date', 'time',)
#         export_order = ('invitation__first_name', 'invitation__last_name', 'invitation__email', 'date', 'time',)

@admin.register(EventType)
class EventTypeImportExport(ImportExportModelAdmin):
    list_display = ['id', 'label', 'label_ar']


@admin.register(InvitationStatus)
class InvitationStatusImportExport(ImportExportModelAdmin):
    list_display = ['id', 'label', 'label_ar']


@admin.register(Event)
class EventImportExport(ImportExportModelAdmin):
    list_display = ['id', 'name', 'user', 'type', 'city', 'country', 'capacity', 'is_active']


@admin.register(Title)
class TitleImportExport(ImportExportModelAdmin):
    list_display = ['id', 'title_en', 'title_ar']


@admin.register(Rank)
class RankImportExport(ImportExportModelAdmin):
    list_display = ['id', 'name_en', 'name_ar']


@admin.register(Invitation)
class InvitationImportExport(ImportExportModelAdmin):
    list_display = ['id', 'event','first_name', 'last_name', 'name', 'mobile', 'email', 'tickets', 'invitation_type', 'role', 'status', 'reference', 'qr', 'invitation', 'is_generated', 'email_sent']
    list_per_page = 50
    search_fields = ['first_name', 'last_name', 'name', 'mobile', 'email', 'role', 'reference']
    list_filter = ['role', 'status', 'is_generated']
    # list_editable = ('team_name',)

    # resource_class = ParticipantResource
    # def get_export_resource_class(self):
    #     return ExportParticipantResource



# @admin.register(Checkin)
# class CheckinImportExport(ImportExportModelAdmin):
#     list_display = ['id', 'invitation', 'date', 'time']
#     list_filter = (
#         ('date', DateRangeFilter), 
#         # ('updated_at', DateTimeRangeFilter),
#     )
#     resource_class = CheckinResource


@admin.register(Order)
class OrderImportExport(ImportExportModelAdmin):
    list_display = ['id', 'name']