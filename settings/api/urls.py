from django.urls import path
from settings.api.views import (
    GeneralByEvent,
    GeneralDetails,
    StaffSettingByEvent,
    StaffSettingByEventDetails,
)



app_name = 'settings'

urlpatterns = [

    # general settings
    path('general/<str:event_id>/list/', GeneralByEvent.as_view(), name='general_by_event'), # GET LIST, POST general event settings
    path('general/details/<str:pk>/', GeneralDetails.as_view(), name='general_details'), # GET, UPDTE and DELETE

    # staff events setting
    path('staff/<str:event_id>/list/', StaffSettingByEvent.as_view(), name='staff_settings_by_event'), # GET LIST, POST user
    path('staff/details/<str:pk>/', StaffSettingByEventDetails.as_view(), name='staff_settings_details'), # GET, UPDTE and DELETE

]