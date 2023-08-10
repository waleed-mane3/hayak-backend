from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.permissions import ClientAccountObjectPermission
# from django.conf import settings
from tablib import Dataset

from account.api.serializers import (
    CreateClientSerializer,
    GetClientSerializer,
    UpdateClientSerializer,
    
    CreateMainAdminSerializer,
    UpdateMainClientSerializer,
    UpdateMainAdminSerializer,
    UpdateUserPasswordSerializer,
    UpdateUserSerializer,
    MainAdminSerializer,
    MainClientSerializer,
    ListUsersSerializer,
    UsersDetailsSerializer,
    CreateAccountsSerializer
    )
from rest_framework.views import APIView
from django.conf import settings
from .queries import *
from utils.errors import Error, APIError




###########################################################################
# ACTION DONE BY CLIENTS ##################################################
###########################################################################

# Create & List Clients ###################################################
@api_view(['POST',])
def client_list(request):

    data = {}
    
    if request.method == 'POST':
        serializer = CreateClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user has been created successfully!"
            request_status = status.HTTP_201_CREATED

        else:
            data['details'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=request_status)
# End Create & List Clients ###############################################


# Get, Update and Delete Client Account (password not included with update)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ClientAccountObjectPermission,])
def client_details(request, pk):
    user = request.user
    data = {}

    # Find user 
    try:
        user = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        data['details'] = "User is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)


    # Checking Permission
    if not ClientAccountObjectPermission().has_object_permission(request, None, user):
        data['details'] = "You don't have permission to perform this action!" 
        request_status = status.HTTP_403_FORBIDDEN
        return Response(data=data, status=request_status)
    

    # Get Client
    if request.method == 'GET':
        print(f"requester: {request.user.id}")
        print(f"object: {user.id}")
        serializer = GetClientSerializer(user)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)
    

    # Update Client 
    if request.method == 'PUT':
        serializer = UpdateClientSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "User has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


    # Delete Client 
    if request.method == 'DELETE':
        operation = user.delete()
        data = {}
        if operation:
            data['success'] = "User has been deleted successfully!"
            request_status = status.HTTP_204_NO_CONTENT
        else:
            data["detail"] = "Something went wrong during the delete operation!"
            request_status = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
###########################################################################



# Update password (Admin & Client) ########################################
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user

    if request.method == "PUT":
        serializer = UpdateUserPasswordSerializer(user, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['details'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=request_status)
# End update password #####################################################














# Update user #######################################################
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = {}

    if request.method == "PUT":
        if user.user_type == 1:
            serializer = UpdateMainAdminSerializer(user, data=request.data)
        elif user.user_type == 2:
            serializer = UpdateMainClientSerializer(user, data=request.data)


        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['error'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=request_status)
# End update user ###################################################




# Get User Info #####################################################
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    data = {}

    if user.user_type == 1:
        serializer = MainAdminSerializer(user)
    if user.user_type == 2:
        serializer = MainClientSerializer(user)

    request_status = status.HTTP_200_OK
    data = serializer.data

    return Response(data=data, status=request_status)
#####################################################################


# Update Event ######################################################
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_account(request):
    user = request.user

    if request.method == "PUT":
        serializer = UpdateUserSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "update successful"
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#####################################################################


# Get Health ########################################################
@api_view(['GET',])
def get_health(request):
    request_status = status.HTTP_200_OK
    return Response(status=request_status)
#####################################################################


# List & Create Event ###############################################
class Account(APIView):
    """Get and create accounts"""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        data = {}

        # Admin return all user of any type
        if user.user_type == settings.ADMIN:
            users = getAllCustomUser()
        elif user.user_type == settings.CLIENT:
            users = getClientUsersAndRelated(user=user)

        serializer = ListUsersSerializer(users, many=True)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)


    def post(self, request, format=None):
        """Create Client and Scanner CustomUser and account (Dynamically for any new account type later on)"""
        user = request.user
        data = {}
        user_type = None
        try:
            user_type = request.data['user_type']
            client_info = request.data['client_info']
            extra_data = request.data['extra_data']
        except Exception as er:
            raise APIError(Error.FEILD_IS_REQUIRED, extra=[str(er)])

        # check password validity else will raise a bug

        serializer = CreateAccountsSerializer(data=request.data, context={'user_type':user_type, 'client_info':client_info, 'extra_data': extra_data})


        if serializer.is_valid(raise_exception=True):
            serializer.save()
            request_status = status.HTTP_201_CREATED
        else:
            request_status = status.HTTP_400_BAD_REQUEST

        return Response(data=serializer.data, status=request_status)
#####################################################################


#####################################################################
class AccountDetails(APIView):
    """Get and create accounts"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        user = getCustomUser(pk=id)
        serializer = UsersDetailsSerializer(user)
        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)


    def patch(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        user = getCustomUser(pk=id)
        serializer = UsersDetailsSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):

            serializer.save()
        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)

    def delete(self, request, *args, **kwargs):
        """Delete will not actually delete, but set the custom user to is_active = False"""
        user = request.user
        data = {}
        id = self.kwargs['pk']
        user = getCustomUser(pk=id)
        serializer = UsersDetailsSerializer(user, data={'is_active': False})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)
#####################################################################