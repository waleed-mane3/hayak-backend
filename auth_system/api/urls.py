from django.urls import path, include
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from account.api.views import update_password




urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('password-update/', update_password, name='update_password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
