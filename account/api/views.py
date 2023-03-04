from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings
from tablib import Dataset

from account.api.serializers import (
    CreateMainClientSerializer, 
    CreateMainAdminSerializer,
    UpdateMainClientSerializer,
    UpdateMainAdminSerializer,
    UpdateUserPasswordSerializer,
    UpdateUserSerializer,
    MainAdminSerializer,
    MainClientSerializer,
    )

from account.models import Client, Admin



# Create Client ###############################################################
@api_view(['POST',])
def create_client(request):

    data = {}
    # try:
    #     user_type = request.data['user_type'] 
    # except:
    #     data['error'] = "user_type must be provided!"
    #     request_status = status.HTTP_400_BAD_REQUEST
    #     return Response(data=data, status=request_status) 
    
    # if user_type != 2:
    #     data['error'] = "user_type must be integer number!"
    #     request_status = status.HTTP_400_BAD_REQUEST
    #     return Response(data=data, status=request_status) 

    
    if request.method == 'POST':
        serializer = CreateMainClientSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user has been created successfully!"
            request_status = status.HTTP_201_CREATED

        else:
            data['error'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)
# End create client ###########################################################


# Update user ##############################################################
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
# End update user ###########################################################



# Update password ##############################################################
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
            data['error'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)
# End update password ###########################################################










# Get User Info #################################################################
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
#################################################################################









# Update Event
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





            

# Get Health
@api_view(['GET',])
def get_health(request):
    request_status = status.HTTP_200_OK
    return Response(status=request_status)