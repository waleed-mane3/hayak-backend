from rest_framework_simplejwt.views import TokenObtainPairView
from auth_system.api.serializers import MyTokenObtainPairSerializer



# Login View ########################################################
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
# End Login View ####################################################


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
