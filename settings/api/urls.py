from django.urls import path
from settings.api.views import (
    GeneralByEvent,
    GeneralDetails,
)



app_name = 'settings'

urlpatterns = [

    # card
    path('general/<str:event_id>/list/', GeneralByEvent.as_view(), name='general_by_event'), # GET LIST, POST user
    path('general/details/<str:pk>/', GeneralDetails.as_view(), name='general_details'), # GET, UPDTE and DELETE

    # # transctions
    # path('trans/list/', Transactions.as_view(), name='transactions'), # GET LIST, POST user
    # path('trans/details/<str:pk>/', TransactionsDetails.as_view(), name='transaction_details'), # GET, UPDTE and DELETE
]