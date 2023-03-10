from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings

from scan.api.serializers import (
    ScanSerializer,
    )

from event.models import Event, Invitation
from scan.models import Scan
from utils.pagination import CustomPagination
from scan.resources import ScansResource



# List & Create Scans
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def scan_list(request, pk):
    user = request.user
    data = {}
    

    # check event existance 
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['detail'] = "This event is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)


    # check if this event belongs to this user 
    if user.user_type == 2:
        if event.user.id != user.id:
            data['detail'] = "This event does not belong to this user!" 
            request_status = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=request_status)

    elif user.user_type == 3:
        scanner_events = user.scanner.events.all().values_list('id', flat=True)
        is_event_existed = False
        for el in scanner_events:
            if el == event.id:
                is_event_existed = True
        
        if is_event_existed == False:
            data['detail'] = "This event does not belong to this user!" 
            request_status = status.HTTP_403_FORBIDDEN
            return Response(data=data, status=request_status)


    # This will bring all event scnas
    if request.method == 'GET':
    
        if user.user_type == 2:
            scans = Scan.objects.filter(event=event) #change to set!!
        elif user.user_type == 3:
            scans = Scan.objects.filter(event=event).filter(scanned_by=user)

        request_status = status.HTTP_200_OK

        if len(scans) > 0:
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(scans, request)
            serializer = ScanSerializer(result_page, many=True)
            data = serializer.data
            return paginator.get_paginated_response(data=data)
        else:
            return Response(data=data, status=request_status)

    



    # This will create new scan for this invitation 
    if request.method == 'POST':
        # check invitation existance 
        try:
            invitation_id = request.data['invitation']
            invitation = Invitation.objects.get(reference=invitation_id)
        except Invitation.DoesNotExist:
            data['detail'] = "This inviation is not found!" 
            request_status = status.HTTP_404_NOT_FOUND
            return Response(data=data, status=request_status)
        
        invitation_event = invitation.event
            
        # check if this invitation belongs to this event 
        if event != invitation_event:
            data['detail'] = "This inviation does not belong to this event!" 
            request_status = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=request_status)


        # check if the number of scans exceeded the tickets no 
        invitation_tickets = invitation.tickets
        invitation_scans = Scan.objects.filter(invitation=invitation).count()
        if invitation_scans >= invitation_tickets:
            # data["id"] = invitation.id
            data['detail'] = "You have reached the limit of scans!"
            data['name'] = f"{invitation.first_name} {invitation.last_name}"
            data['event_name'] = invitation.event.name
            data['invitation_type'] = invitation.invitation_type
            data["total"] = invitation_tickets
            data["used"] = invitation_scans
            data["unused"] = invitation_tickets - invitation_scans
            request_status = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=request_status)


        serializer = ScanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event, invitation=invitation, scanned_by=user)
            invitation_to_update = Invitation.objects.filter(reference=invitation_id)
            invitation = Invitation.objects.filter(reference=invitation_id).first()
            invitation_to_update.update(status=3) # this has to by dynamic


            invitation_tickets = invitation.tickets
            invitation_scans = Scan.objects.filter(invitation=invitation).count()
            # data["id"] = invitation.id
            data['success'] = "Scan Success!"
            data['name'] = f"{invitation.first_name} {invitation.last_name}"
            data['event_name'] = invitation.event.name
            data['invitation_type'] = invitation.invitation_type
            data["total"] = invitation_tickets
            data["used"] = invitation_scans
            data["unused"] = invitation_tickets - invitation_scans
            request_status = status.HTTP_201_CREATED
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=request_status)






# Export Scans #####################################################################
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def export_scans(request):
    user = request.user
    if request.method == 'GET':
        # Get selected option from form
        file_format = "XLS"

        try:
            event_id = request.GET["event"]
            event = Event.objects.get(id=int(event_id))
        except:
            data["details"] = "You must provide the event id!" 
            request_status = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=request_status)

        scans = Scan.objects.filter(event=event)

        if user.id != event.user.id:
            data["detail"] = "This event does not belong to this client!" 
            request_status = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=request_status)

        scans_resource = ScansResource()
        dataset = scans_resource.export(scans)
        data = {}

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
         
    return response
#####################################################################################









# Update Invitation for Event (cleaned)
# @api_view(['PUT',])
# @permission_classes([IsAuthenticated])
# def scan_invitation(request, pk):
#     try:
#         invitation = Invitation.objects.get(id=pk)
#     except Invitation.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     data_to_update = {'status': 'checked'}
#     if request.method == "PUT":
#         serializer = ScanInvitationSerializer(invitation, data=data_to_update)
#         print(serializer)
#         data = {}

#         if serializer.is_valid():
#             serializer.save()
#             data['success'] = "Invitation Scanned successful!"
#             request_status = status.HTTP_200_OK
#         else:
#             data['error'] = "Scanning went wrong!"
#             data['details'] = serializer.errors
#             request_status = status.HTTP_400_BAD_REQUEST
        
#         return Response(data=data, status=request_status)
