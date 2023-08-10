from django.urls import path
from account.api.views import (
    client_list,
    client_details,

    user_info,
    update_user,
    Account,
    AccountDetails,
)

app_name = 'account'

urlpatterns = [
    # Client APIs
    path('client/user/list/', client_list, name='client_list'), # client only
    path('client/user/details/<str:pk>/', client_details, name='client_details'), # client only


    path('user/info/', user_info, name='user_info'), # admin, client
    path('user/update/', update_user, name='update_client'), # admin, client

    # path('user/list/', register_user, name='register_client'), # only client
    # path('user/info/', user_info, name='user_info'), # admin, client
    # path('user/update/', update_user, name='update_client'), # admin, client


    # Account
    path('list/', Account.as_view(), name='client_accounts'), # GET LIST, POST USER
    path('details/<str:pk>/', AccountDetails.as_view(), name='account_details'), # GET, UPDTE and DELETE
]
