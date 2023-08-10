from import_export import resources
from import_export.fields import Field
from scan.models import Scan
# https://www.letscodemore.com/blog/django-import-export-from-basic-to-advance/#resources_django


class ScansResource(resources.ModelResource):
    pass
    # scanned_by = Field(column_name='scanned_by')
    
    # def dehydrate_scanned_by(self, obj):

    #     scanned_by = f"{obj.scanned_by.first_name} {obj.scanned_by.last_name}"

    #     return scanned_by


    # class Meta:
    #     model = Scan
    #     fields = (
    #         "invitation__first_name",
    #         "invitation__last_name",
    #         "invitation__email",
    #         "invitation__mobile",
    #         "invitation__tickets",
    #         "invitation__invitation_type",
    #         "scanned_by",
    #         "date",
    #         "time"
    #     )
    #     export_order = (
    #         "invitation__first_name",
    #         "invitation__last_name",
    #         "invitation__email",
    #         "invitation__mobile",
    #         "invitation__tickets",
    #         "invitation__invitation_type",
    #         "scanned_by",
    #         "date",
    #         "time"
    #     )
    #     skip_unchanged = True
    #     report_skipped = True

        