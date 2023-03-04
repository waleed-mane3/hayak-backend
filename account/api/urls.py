from django.urls import path
from account.api.views import (
    user_info,
    create_client, 
    update_user,
)

app_name = 'account'

urlpatterns = [
    # user
    path('user/info/', user_info, name='user_info'), # admin, client
    path('user/create/', create_client, name='create_client'), # only client
    path('user/update/', update_user, name='update_client'), # admin, client


    # Account 
    # path('event/list/', update_user, name='update_client'), # GET LIST, POST user
    # path('event/details/<str:pk>/', update_user, name='update_client'), GET, UPDTE and DELETE
]
