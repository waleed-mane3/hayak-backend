from django.urls import path
from account.api.views import (
    user_info,
    create_client,
    update_user,
    Account,
    AccountDetails,
)

app_name = 'account'

urlpatterns = [
    # user
    path('user/info/', user_info, name='user_info'), # admin, client
    path('user/create/', create_client, name='create_client'), # only client
    path('user/update/', update_user, name='update_client'), # admin, client


    # Account
    path('list/', Account.as_view(), name='client_accounts'), # GET LIST, POST user
    path('details/<str:pk>/', AccountDetails.as_view(), name='account_details'), # GET, UPDTE and DELETE
]
