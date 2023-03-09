from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
# from django.conf import settings
from event.resources import InvitationResource
from tablib import Dataset

from event.api.serializers import (
    EventSerializer,
    EventsSerializer,
    InvitationSerializer,
    EventTypeSerializer,
    InvitationStatusSerializer,
    UpdateEventSerializer,
    UpdateInvitationSerializer,
    
    CreateEventSerializer,  
    UserEventsSerializer, 
    CreateInvitationSerializer, 
    EventInvitationsSerializer, 
    # UpdateInvitationSerializer, 
    # ScanInvitationSerializer
)
from webhook.models import AcmeWebhookMessage
import json
from django.utils import timezone


from account.models import Client, Admin
from event.models import Event, Invitation, EventType, InvitationStatus, Order
from account.functions import send_confirmation_email

from event.permissions import EventOwnerOrReadOnly
# https://stackoverflow.com/questions/34043378/how-to-paginate-response-from-function-based-view-of-django-rest-framework
from rest_framework.pagination import PageNumberPagination
from utils.pagination import CustomPagination

# # qr packages 
# from PIL import Image, ImageDraw, ImageFilter, ImageFont
# import pyqrcode
# import arabic_reshaper
# from bidi.algorithm import get_display
# import urllib.request

from utils.emails import *
import time
from django.conf import settings





# List & Create Event ###############################################
class EventList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        data = {}

        # Get object 
        if user.user_type == settings.CLIENT:
            events = Event.objects.filter(user=user)
        elif user.user_type == 3:
            events = user.scanner.events.all()


        serializer = EventsSerializer(events, many=True)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)


    def post(self, request, format=None):
        user = request.user
        data = {}
        
        if user.user_type != settings.CLIENT:
            data['detail'] = "You need higher permission!" 
            request_status = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=request_status)


        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            data['success'] = "Event has been created successfully!"
            request_status = status.HTTP_201_CREATED
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)
#####################################################################
        



# Get, Update and Delete User Events ################################
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_details(request, pk):
    user = request.user
    data = {}

    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['detail'] = "This event is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)

    # permissions 
    if user.user_type == 2:
        if event.user.id != user.id:
            data['detail'] = "You are not authorizated!" 
            request_status = status.HTTP_403_FORBIDDEN
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


    
    # Get Event 
    if request.method == 'GET':
        serializer = EventSerializer(event)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)
    

    # Update Event 
    if request.method == 'PUT':
        serializer = UpdateEventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Event has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


    # Delete Event 
    if request.method == 'DELETE':
        operation = event.delete()
        data = {}
        if operation:
            data['success'] = "Event has been deleted successfully!"
            request_status = status.HTTP_204_NO_CONTENT
        else:
            data["detail"] = "Something went wrong during the delete operation!"
            request_status = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
#####################################################################




# List & Create Envitations #########################################
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def invitation_list(request, pk):
    user = request.user
    data = {}

    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['detail'] = "This event is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)

    if event.user.id != user.id:
        data['detail'] = "You are not authorizated!" 
        request_status = status.HTTP_403_FORBIDDEN
        return Response(data=data, status=request_status)


    # This will bring all user event Invitations 
    if request.method == 'GET':

        invitations = Invitation.objects.filter(event=event).order_by("-id") #change to set!!
        request_status = status.HTTP_200_OK

        if len(invitations) > 0:
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(invitations, request)
            serializer = InvitationSerializer(result_page, many=True)
            data = serializer.data
            return paginator.get_paginated_response(data=data)
        else:
            return Response(data=data, status=request_status)

    


    # This will create new invitation for this user 
    if request.method == 'POST':
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event)
            data['success'] = "Invitation has been created successfully!"
            request_status = status.HTTP_201_CREATED
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=request_status)
#####################################################################




# Get, Update and Delete Event Invitations ##########################
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def invitation_details(request, pk, pk2):
    user = request.user
    data = {}


    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['detail'] = "This event is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)

    if event.user.id != user.id:
        data['detail'] = "You are not authorizated!" 
        request_status = status.HTTP_403_FORBIDDEN
        return Response(data=data, status=request_status)


    try:
        invitation = Invitation.objects.get(id=pk2)
    except Invitation.DoesNotExist:
        data['detail'] = "This invitation is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)
    

    if invitation.event != event:
        data['detail'] = "You are not authorizated!" 
        request_status = status.HTTP_403_FORBIDDEN
        return Response(data=data, status=request_status)

    
    # Get Invitation 
    if request.method == 'GET':    
        serializer = InvitationSerializer(invitation)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)
    

    # Update Invitation 
    if request.method == 'PUT':
        serializer = UpdateInvitationSerializer(invitation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Invitation has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


    # Delete Invitation 
    if request.method == 'DELETE':
        operation = invitation.delete()
        data = {}
        if operation:
            data['success'] = "Invitation has been deleted successfully!"
            request_status = status.HTTP_204_NO_CONTENT
        else:
            data["detail"] = "Something went wrong during the delete operation!"
            request_status = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
#####################################################################




# List Event Types ##################################################
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def eventtype_list(request):
    
    user = request.user
    data = {}
    
    # This will bring all user events 
    if request.method == 'GET':
        eventtypes = EventType.objects.all()
        serializer = EventTypeSerializer(eventtypes, many=True)
        data = serializer.data
        request_status = status.HTTP_200_OK
    

    return Response(data=data, status=request_status)
#####################################################################


# List Invitations Status ###########################################
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def invitation_status_list(request):
    
    user = request.user
    data = {}
    
    # This will bring all Invitation Statuss
    if request.method == 'GET':
        invitation_statuss = InvitationStatus.objects.all()
        serializer = InvitationStatusSerializer(invitation_statuss, many=True)
        data = serializer.data
        request_status = status.HTTP_200_OK
    
    return Response(data=data, status=request_status)
#####################################################################



# List & Create Rank ###############################################
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def rank_list(request):
    
    user = request.user
    data = {}
    
    # This will bring all user events 
    if request.method == 'GET':
        events = Event.objects.filter(user=user)
        serializer = EventSerializer(events, many=True)
        data = serializer.data
        request_status = status.HTTP_200_OK
    
    # This will create new event for this user 
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            data['success'] = "Event has been created successfully!"
            request_status = status.HTTP_201_CREATED
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=request_status)
#####################################################################


# Get, Update and Delete Rank ################################
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def rank_details(request, pk):
    user = request.user
    data = {}

    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        data['detail'] = "This event is not found!" 
        request_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=request_status)

    if event.user.id != user.id:
        data['detail'] = "You are not authorizated!" 
        request_status = status.HTTP_403_FORBIDDEN
        return Response(data=data, status=request_status)

    
    # Get Event 
    if request.method == 'GET':
        serializer = EventSerializer(event)
        data = serializer.data
        request_status = status.HTTP_200_OK
        return Response(data=data, status=request_status)
    

    # Update Event 
    if request.method == 'PUT':
        serializer = UpdateEventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Event has been updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['detail'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


    # Delete Event 
    if request.method == 'DELETE':
        operation = event.delete()
        data = {}
        if operation:
            data['success'] = "Event has been deleted successfully!"
            request_status = status.HTTP_204_NO_CONTENT
        else:
            data["detail"] = "Something went wrong during the delete operation!"
            request_status = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
#####################################################################







# Send bulk emails #########################################
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def emails_view(request):
    user = request.user
    data = {}

    # print(request.data['ids'])
    # print(type(request.data['ids']))
    try:
        guest_ids = []
        ids = request.data['ids']
        for item in ids.split(","):
            guest_ids.append(int(item))
    except:
        guest_ids = []


    # This will bring all user event Invitations 
    if request.method == 'POST':

        # if guest_ids:
        for guest_id in guest_ids:
            invitation_to_update = Invitation.objects.filter(id=guest_id)

            if invitation_to_update.count() > 0:
                invitation = invitation_to_update.first()
                # send email 
                invitation_email(
                    f"{invitation.first_name} {invitation.last_name}",
                    invitation.email,
                    invitation.event.name,
                    str(invitation.event.date.date()),
                    invitation.event.location,
                    invitation.qr.url,
                    invitation.event.venue,
                    invitation.event.city,
                    invitation.event.user.image.url,
                    invitation.event.user.first_name,
                    invitation.entries,
                    invitation.invitation_type
                )
                invitation_to_update.update(email_sent=True)
        
        data["success"] = "Emails sent successfully!"
        request_status = status.HTTP_200_OK

    return Response(data=data, status=request_status)
#####################################################################








# Import invitations ################################################
@api_view(['POST',])
# @permission_classes([IsAuthenticated])
def invitations_import(request, pk):
    data = {}
    
    event = Event.objects.get(id=pk)
    # event_capacity = event.capacity
    # print(f"Event Capacity: {event_capacity}")

    # current_invitations = event.invitation_set.all().count()
    # print(f"Current Invitations: {current_invitations}")

    # allowed = event_capacity - current_invitations
    # print(f"Allowed to Add: {allowed}")


    
    if request.method == 'POST':
        file_format = 'CSV'
        invitations_resource = InvitationResource()
        dataset = Dataset()
        new_guests = request.FILES['file']

        if file_format == 'CSV':
            imported_data = dataset.load(new_guests.read().decode('utf-8'),format='csv')
            dataset_count = len(dataset)
            event_list_ids = [int(pk)] * dataset_count
            dataset.append_col(event_list_ids, header='event')
            
            # if dataset_count <= allowed:
            result = invitations_resource.import_data(dataset, dry_run=True) 
            data['success'] = "Import has been done successfully!"
            request_status = status.HTTP_200_OK

            # else:
            #     data['error'] = "your imported file exceeded your package invitations"
            #     data['allowed'] = allowed
            #     request_status = status.HTTP_400_BAD_REQUEST

        # if dataset_count <= allowed:
        if not result.has_errors():
            # Import now
            invitations_resource.import_data(dataset, dry_run=False)
    

    return Response(data=data, status=request_status) 
#####################################################################


# Webhook test ###############################################
@api_view(['POST'])
def webhook(request):
    
    
    Order.objects.create(
        name=request.data['name']
    )
    
    request_status = status.HTTP_200_OK

    return Response({"success": "done"}, status=request_status)
#####################################################################




# # Generate Invitations ##############################################
# # make transparent bg function 
# def convertImage(url):
#     # img = Image.open(f"static/images/qr/invitations/{url}")
#     img = urllib.request.urlopen(url)
#     img = img.convert("RGBA")
#     datas = img.getdata()
#     newData = []

#     for item in datas:
#         if item[0] == 255 and item[1] == 255 and item[2] == 255:
#             newData.append((255, 255, 255, 0))
#         else:
#             newData.append(item)

#     img.putdata(newData)
#     img.save(f"static/images/qr/trans/{url}", "PNG")


# create qr code function 
# def create_qr(visitor_id, url):
#     link = pyqrcode.create(visitor_id)
#     link.png(f'static/images/qr/invitations/{url}', scale=20, module_color="#000000", background="#fff")



# @api_view(['GET',])
# # @permission_classes([IsAuthenticated])
# def generate_invitations(request,pk):
#     data = {}
#     try:
#         invitation = Invitation.objects.filter(id=pk)
#     except:
#         data['detail'] = "This invitation is not found!" 
#         request_status = status.HTTP_404_NOT_FOUND
#         return Response(data=data, status=request_status)
    

#     if invitation.is_generated == True:
#         data['detail'] = "Invitation has been generated!" 
#         request_status = status.HTTP_400_BAD_REQUEST
#         return Response(data=data, status=request_status)
    
        

#     # Create Invitation Card ##################################
#     # card = Image.open("static/images/card/card.png")
#     card = urllib.request.urlopen(invitation.qr)
    
    
#     # add text 
#     W, H = 400, 550
#     raw_msg = f"{invitation.first_name} {invitation.last_name}"
#     msg_reshaped = arabic_reshaper.reshape(raw_msg)
#     msg = get_display(msg_reshaped , base_dir='R')

#     # im = Image.new("RGBA",(W,H),"yellow")
#     draw = ImageDraw.Draw(card)
#     myFont = ImageFont.truetype("static/font/azer.ttf", 39)
#     w, h = draw.textsize(msg, font=myFont)
#     draw.text(((W-w)/2,(H-h)/2), msg, fill="#000000", font = myFont, stroke_width=1, stroke_fill="#000000")
#     # End add text


#     # im2 = Image.open(fr"C:\Users\WALEEDMANE3\Desktop\People\Bamashmos\wedding\methaq\static\images\qr\trans\{fqr_url}")
#     im2 = Image.open(f"static/images/qr/trans/{fqr_url}")
#     size = (150, 150)
#     im2.thumbnail(size)

#     back_card = card.copy()
#     back_card.paste(im2, ((W-size[0])//2, (H+60)//2), im2)
#     # back_card.save(fr"C:\Users\WALEEDMANE3\Desktop\People\Bamashmos\wedding\methaq\static\images\invitations\{visitor.visitor_id}-{visitor.id}.jpg", quality=200)
#     back_card.save(f"static/images/invitations/{invitation.id}.png", quality=200)
#     # End Create Invitation Card ##############################
        

#     data['success'] = "All invitations generated successfully!"
#     request_status = status.HTTP_200_OK

    
    
#     return Response(data=data, status=request_status)
# #############################################################################

























                    

# Create New Event for user 
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def create_event(request):
    
    if request.method == "POST":
        print(request.data)
        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    
    return Response(serializer.data)









# Update Event
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = UpdateEventSerializer(event, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "update successful"
            return Response(data=data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Delete Event
@api_view(['DELETE',])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        operation = event.delete()
        data = {}
        if operation:
            data['success'] = "delete successful"
            # stat = status.HTTP_200_OK

        else:
            data["failure"] = "delete failed"
            # stat = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data)





# Get all events for user
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def all_user_events(request):
    user = request.user
    events = user.event_set.all()
    serializer = UserEventsSerializer(events, many=True)
    return Response(serializer.data)





# Create New Invitation for Event 
@api_view(['POST',])
@permission_classes([IsAuthenticated])
def create_invitation(request):
    
    if request.method == "POST":
        serializer = CreateInvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    
    return Response(serializer.data)





# Get all Invitations for Event
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def all_event_invitations(request, pk):
    event = Event.objects.get(id=pk)
    invitations = event.invitation_set.all()
    serializer = EventInvitationsSerializer(invitations, many=True)
    return Response(serializer.data)





# Update Invitation for Event (cleaned)
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_invitation(request, pk):

    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = UpdateInvitationSerializer(invitation, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Invitation updated successfully!"
            request_status = status.HTTP_200_OK
        else:
            data['error'] = "Somthing went wrong!"
            data['details'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)


# Update Invitation for Event (cleaned)
@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def scan_invitation(request, pk):
    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data_to_update = {'status': 'checked'}
    if request.method == "PUT":
        serializer = ScanInvitationSerializer(invitation, data=data_to_update)
        print(serializer)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data['success'] = "Invitation Scanned successful!"
            request_status = status.HTTP_200_OK
        else:
            data['error'] = "Scanning went wrong!"
            data['details'] = serializer.errors
            request_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data=data, status=request_status)




# Delete Invitation for Event
@api_view(['DELETE',])
@permission_classes([IsAuthenticated])
def delete_invitation(request, pk):
    try:
        invitation = Invitation.objects.get(id=pk)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        operation = invitation.delete()
        data = {}
        if operation:
            data['success'] = "delete successful"
            # stat = status.HTTP_200_OK

        else:
            data["failure"] = "delete failed"
            # stat = status.HTTP_501_NOT_IMPLEMENTED

        return Response(data=data)



# Get all Invitations for Event
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def confirmation_email(request, pk):
    user = request.user
    invitation_filtered = Invitation.objects.filter(id=pk)
    invitation = invitation_filtered.first()
    data = {}

    if invitation.status == "pending":
        invitation_filtered.update(status="waiting")
        send_confirmation_email(user.first_name, invitation.name, invitation.email, invitation.reference)
        data['success'] = "email sent"
        request_status = status.status.HTTP_200_OK
    else:
        data['error'] = "You have already send a confirmation email to this invitee!"
        request_status = status.HTTP_400_BAD_REQUEST

    return Response(data, status=request_status)



# Accept Invitation
def accept_invitation(request, pk):
    
    try:
        invitation = Invitation.objects.filter(reference=pk)
        if invitation.first().status == "waiting":
            invitation.update(status="confirmed")
            return HttpResponse("<h1>Invitation has been accepted!</h1>")
        else:
            return HttpResponse("<h1>This link has been used already!</h1>")

    except:
        return HttpResponse("<h1>Something went wrong!</h1>")


# Reject Invitation
def reject_invitation(request, pk):
    
    try:
        invitation = Invitation.objects.filter(reference=pk)
        if invitation.first().status == "waiting":
            invitation.update(status="apologized")
            return HttpResponse("<h1>Invitation has been rejected!</h1>")
        else:
            return HttpResponse("<h1>This link has been used already!</h1>")

    except:
        return HttpResponse("<h1>Something went wrong!</h1>")
    




def export_guests(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        employee_resource = InvitationResource()
        dataset = employee_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'design/export.html')



 
# # List & Create Event ###############################################
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def event_list(request):
    
#     user = request.user
#     data = {}
    
#     # This will bring all user events 
#     if request.method == 'GET':
#         events = Event.objects.filter(user=user)
#         serializer = EventSerializer(events, many=True)
#         data = serializer.data
#         request_status = status.HTTP_200_OK
    
#     # This will create new event for this user 
#     if request.method == 'POST':
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user)
#             data['success'] = "Event has been created successfully!"
#             request_status = status.HTTP_201_CREATED
#         else:
#             data['detail'] = serializer.errors
#             request_status = status.HTTP_400_BAD_REQUEST

#     return Response(data=data, status=request_status)
# #####################################################################