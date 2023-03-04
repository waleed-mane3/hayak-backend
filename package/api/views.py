from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings
from package.api.serializers import (
    PackageSerializer,
    )
from package.models import Package




# List & Create Package
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def package_list(request):
    # user = request.user
    data = {}
    
    # This will bring all packages
    if request.method == 'GET':
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        data = serializer.data
        request_status = status.HTTP_200_OK
    
    # This will create new package
    if request.method == 'POST':
        serializer = PackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Package has been created successfully!"
            request_status = status.HTTP_201_CREATED
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=request_status)




# Get, Update and Delete Package
@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def package_details(request, pk):
    # user = request.user
    data = {}


    try:
        package = Package.objects.get(id=pk)
    except Package.DoesNotExist:
        data['detail'] = "This package is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)

    
    # Get Package 
    if request.method == 'GET':    
        serializer = PackageSerializer(package)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)
    

    # Update Package 
    if request.method == 'PUT':
        serializer = PackageSerializer(package, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Package has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


    # Delete Package 
    if request.method == 'DELETE':
        operation = package.delete()
        data = {}
        if operation:
            data['success'] = "Package has been deleted successfully!"
            request_status = status.HTTP_204_NO_CONTENT
        else:
            data["detail"] = "Something went wrong during the delete operation!"
            request_status = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)



