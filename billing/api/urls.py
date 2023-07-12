from django.urls import path
from billing.api.views import (
    Cards,
    CardsDetails,
    Transactions,
    TransactionsDetails
)


app_name = 'billing'

urlpatterns = [

    # card
    path('card/list/', Cards.as_view(), name='cards'), # GET LIST, POST user
    path('card/details/<str:pk>/', CardsDetails.as_view(), name='cards_details'), # GET, UPDTE and DELETE

    # transctions
    path('trans/list/', Transactions.as_view(), name='transactions'), # GET LIST, POST user
    path('trans/details/<str:pk>/', TransactionsDetails.as_view(), name='transaction_details'), # GET, UPDTE and DELETE
]