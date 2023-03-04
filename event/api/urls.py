from django.urls import path
from event.api.views import (
    EventList,
    event_details,
    invitation_details,
    invitation_list,

    eventtype_list,
    invitation_status_list,
 
    invitations_import,
    webhook,

    emails_view
)

app_name = 'event'

urlpatterns = [
    # # Events 
    path('list/', EventList.as_view(), name="event_list"),
    path('details/<str:pk>/', event_details, name="event_details"),

    ## Invitations
    path('<str:pk>/invitation/list/', invitation_list, name="invitation_list"),
    path('<str:pk>/invitation/details/<str:pk2>/', invitation_details, name="invitation_details"),

    # Event types 
    path('lookup/event-types/', eventtype_list, name="eventtypes_list"),
    path('lookup/invitation-statuses/', invitation_status_list, name="invitation_status_list"),

    # Import invitations
    path('<str:pk>/invitation/import/', invitations_import, name='inviations_import'),
    path('webhook/', webhook, name='webhook'),

    # Emails
    path('send/emails/', emails_view, name="emails_view"),




    # # Events 
    # path('create_event/', create_event),
    # path('update_event/<str:pk>/', update_event),
    # path('delete_event/<str:pk>/', delete_event),
    # path('user_events/', all_user_events),
    # # Invitations
    # path('create_invitation/', create_invitation),
    # path('event_invitations/<str:pk>/', all_event_invitations),
    # path('update_invitation/<str:pk>/', update_invitation),
    # path('scan_invitation/<str:pk>/', scan_invitation),
    # path('delete_invitation/<str:pk>/', delete_invitation),
    # path('export_guests/', export_guests, name='export_guests'),
    # path('import_guests/<str:pk>/', import_guests, name='import_guests'),
    # # Confirming Invitation
    # path('accept_invitation/<str:pk>/', accept_invitation),
    # path('reject_invitation/<str:pk>/', reject_invitation),
    # # Emails
    # path('confirmation_email/<str:pk>/', confirmation_email),
]
