from django.urls import path
from package.api.views import (
    package_list,
    package_details,
)

app_name = 'package'

urlpatterns = [
    path('list/', package_list, name="package_list"),
    path('details/<str:pk>/', package_details, name="package_details"),
]
