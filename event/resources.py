from import_export import resources
from event.models import Invitation 

class InvitationResource(resources.ModelResource):
    class Meta:
        model = Invitation