from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from auth_system.models import CustomUser
from account.models import Client, Admin, Scanner, Regular, DataEntry
from django.conf import settings
from utils.validators import custom_password_validator





class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['user']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['user']




## Create Account serializer ############################################################################################
class CreateAccountsSerializer(serializers.ModelSerializer):
    """Create a Account serializer"""


    class Meta:
        model= CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}, #this will prevent users to read the password when it is passed through the request
            'first_name': {'required': True}, # as required field
            'last_name': {'required': True}, # as required field
            'email': {'required': True}, # as required field
            'mobile': {'required': True} # as required field
        }


    def save(self):

        # Validate the incoming custom fields
        client_type = None
        user_type = None
        client_data = None
        try:
            user_type = self.context.get("user_type")
            client_data = self.context.get("client_info")
            client_type = client_data['client_type']
            ## Extra data will be slightly diff from client type
            extra_data = self.context.get("extra_data")
        except Exception as e:
            raise serializers.ValidationError(f"{e}: field is Required")



        # Mapping model per user incoming data
        def fetchModel(vlaue):
            switcher = {
                1: Admin,
                2: Client,
                3: Regular,
                4: Scanner,
                5: DataEntry,
            }
            return switcher.get(vlaue, vlaue)


        def UpdateClientFieldTypeBoolen(inctance, client_type):
            """update client account type is regular or scanner or data entry"""
            if client_type == 3:
                inctance.is_regular = True
            if client_type == 4:
                inctance.is_scanner = True
            if client_type == 5:
                inctance.is_data_entry = True
            inctance.save()
            return inctance


        # Passowrd Validator Custom for specification else will raise Custom Error
        passowrd_check = custom_password_validator(passowrd=self.validated_data['password'], useremail=self.validated_data['email'])


        ### Doing the check of the NONE for the type cuz there is old endpoint useed it and no conflict

        if user_type != settings.CLIENT and user_type != settings.ADMIN:
            raise serializers.ValidationError("User type is Not officially supported")



        ## Create Custom user with user_type
        user = CustomUser(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            mobile = self.validated_data['mobile'],
            email = self.validated_data['email'],
            user_type = user_type
        )

        password = self.validated_data['password']
        user.set_password(password)

        user.save()


        ## END Create Custom user

        ## Create Main account by Custom user instance ADMIN or CLIENT
        AccountModel = fetchModel(user_type)
        account = AccountModel.objects.create(user=user)
        ## END Create Main account by Custom user instance ADMIN or CLIENT


        # Creating sub Client model by the Client user type
        if user_type == settings.CLIENT:
            ClientModel = fetchModel(client_type)
            # extra_data empty but required in the post, for future use
            user = ClientModel.objects.create(user=account, **extra_data)
            UpdateClientFieldTypeBoolen(account, client_type)


        return user
# End create Client #####################################################################################################################


## Update Client serializer #############################################################################################################
class UpdateMainClientSerializer(serializers.ModelSerializer):

    extra_info = ClientSerializer()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'mobile', 'extra_info',)


    def update(self, instance, validated_data):
        client_data = validated_data.pop('extra_info')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()

        client = Client.objects.filter(user=instance).first()

        if client:
            client.field = client_data.get('field', client.field)
            client.is_assistant = client_data.get('is_assistant', client.is_assistant)
            client.save()

        return instance
# End update client ####################################################################################################################################



## Create admin serializer ############################################################################################
class CreateMainAdminSerializer(serializers.ModelSerializer):
    extra_info = AdminSerializer()

    class Meta:
        model= CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'password', 'extra_info']
        extra_kwargs = {
            'password': {'write_only': True}, #this will prevent users to read the password when it is passed through the request
        }


    # The first_name validation
    def validate_first_name(self, value):

        if value == "":
            raise serializers.ValidationError("First name may not be blank!")
        else:
            return value

    # The last_name validation
    def validate_last_name(self, value):

        if value == "":
            raise serializers.ValidationError("Last name may not be blank!")
        else:
            return value

    # The mobile validation
    def validate_mobile(self, value):

        if value == "":
            raise serializers.ValidationError("Last name may not be blank!") # you need to add numbers validation
        else:
            return value


    # Password cannot be the same as the Email
    def validate(self, data):
        if data['email'] == data["password"]:
            raise serializers.ValidationError("The passward cannot be the same as your email")


    # The Passowrd validation
    def validate_password(self, value):

        if len(value) < 6 or len(value) > 12:
            raise serializers.ValidationError("Password must between 6 - 12 characters")
        else:
            return value



    def save(self):
        user = CustomUser(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            mobile = self.validated_data['mobile'],
            email = self.validated_data['email'],
            user_type = 1
        )

        password = self.validated_data['password']
        # if password != password2:
        #     raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        # Create admin profile
        admin_data = self.validated_data.pop('extra_info')
        Admin.objects.create(user=user, **admin_data)

        return user
# End create admin #####################################################################################################################

## Update admin serializer #############################################################################################################
class UpdateMainAdminSerializer(serializers.ModelSerializer):

    extra_info = AdminSerializer()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'mobile', 'extra_info',)


    def update(self, instance, validated_data):
        admin_data = validated_data.pop('extra_info')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()

        admin = Admin.objects.filter(user=instance).first()

        if admin:
            admin.field = admin_data.get('field', admin.field)
            admin.save()

        return instance
# End update client ####################################################################################################################################


# update password for all users
## Update serializer #############################################################################################################
class UpdateUserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("password",)

    extra_kwargs = {
            'password': {'write_only': True},
        }


    # The Passowrd validation
    def validate_password(self, value):

        if len(value) < 6 or len(value) > 15:
            raise serializers.ValidationError("Password must between 6 - 15 characters")
        else:
            return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
# End update password for all users ####################################################################################################################################






## Info Admin serializer #############################################################################################################
class MainAdminSerializer(serializers.ModelSerializer):

    admin = AdminSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'user_type', 'admin',)
# End Info Admin #####################################################################################################################

## Info Client serializer #############################################################################################################
class MainClientSerializer(serializers.ModelSerializer):

    client = ClientSerializer(read_only=True)


    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'user_type', 'client',)
# End Info Client #####################################################################################################################










# This is used to update #first_sign_in# field
class UpdateUserSerializer(ModelSerializer):
    class Meta:

        model = CustomUser
        fields = ['id', 'first_name', 'first_sign_in', ]


##List all users with all type if Client will return all staff of any type
class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ('user_permissions', 'groups', 'first_sign_in', 'password', )


### For user details get a user, update or delete
class UsersDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ('user_permissions', 'groups', 'password', )
        read_only_fields = ('email',)