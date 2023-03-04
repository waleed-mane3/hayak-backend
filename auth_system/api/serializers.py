from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from auth_system.models import CustomUser


# this is responsible to show information about the user after decode it 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "password",)

    # Make sure the email is in lower case 
    def validate_email(self, value):
        return value.lower()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email_address'] = user.email
        token['mobile'] = user.mobile
        token['user_type'] = user.user_type
        token['first_sign_in'] = user.first_sign_in
        # ...

        return token