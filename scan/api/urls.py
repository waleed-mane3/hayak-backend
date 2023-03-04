from django.urls import path
from scan.api.views import (
    scan_list,
    # scan_details,
)

app_name = 'scan'

urlpatterns = [
    # Scans 
    path('event/<str:pk>/scan/list/', scan_list, name="scan_list"),
    # path('event/<str:pk>/scan/details/<str:pk2>/', scan_details, name="scan_details"),   
]
