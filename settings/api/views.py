from account.permissions import UserTypeAccessAdminOrClient
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from settings.api.queries import (
    getAllGeneral,
    getEventGeneralSettings,
    getGeneralPk,
    getEventStaffSettings,
    getEventStaffSettingsPk,
    getEventSettingsbyEvent,
    getEventSettingsbyEventPk,
)
from settings.api.serializers import (
    ListGeneralSerializer,
    ListStaffSettingsSerializer,
    ListEventSettingsbyEventSerializer,
)


# List & Create General per event ###############################################
class GeneralByEvent(APIView):
    """Get and create General per event"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        user = request.user
        data = {}
        # check if user is admin return all cards in sys
        # else just the client ones
        general = None

        general = getEventGeneralSettings(event_id=int(event_id))
        serializer = ListGeneralSerializer(general, many=True)


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)

    #### No need for post since we create by default once event is created #################################

# END List General per event  ###############################################


# START get update and delete General  ###############################################

class GeneralDetails(APIView):
    """Get, update and delete General Setting per event """

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        general = getGeneralPk(pk=id)
        serializer = ListGeneralSerializer(general)

        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)





    def patch(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        general = getGeneralPk(pk=id)
        serializer = ListGeneralSerializer(general, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)



    def delete(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        general = getGeneralPk(pk=id)
        general.delete()


        request_status = status.HTTP_204_NO_CONTENT
        return Response(status=request_status)

# END get update and delete General  ###############################################


# List staff setting per event ###############################################
class StaffSettingByEvent(APIView):
    """Get and create General per event"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        user = request.user
        data = {}
        # check if user is admin return all cards in sys
        # else just the client ones
        general = None

        general = getEventStaffSettings(event_id=int(event_id))
        serializer = ListStaffSettingsSerializer(general, many=True)


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)

    #### No need for post since we create by default once event is created #################################

# END List staff setting per event  ###############################################

class StaffSettingByEventDetails(APIView):
    """Get, update and delete staff Setting per event """

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]


    ##### GET is not applicable to staff settings (need more details to the figma design)
    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     data = {}
    #     id = self.kwargs['pk']
    #     staff = getEventStaffSettingsPk(pk=id)
    #     serializer = getStaffSettingsSerializer(general)

    #     request_status = status.HTTP_200_OK
    #     return Response(data=serializer.data, status=request_status)




    ##### Action not clear yet to update !!! #################################
    # def patch(self, request, *args, **kwargs):
    #     user = request.user
    #     data = {}
    #     id = self.kwargs['pk']
    #     staff = getGeneralPk(pk=id)
    #     serializer = ListGeneralSerializer(general, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()


    #     request_status = status.HTTP_200_OK
    #     return Response(data=serializer.data, status=request_status)



    def delete(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        staff = getEventStaffSettingsPk(pk=id)
        staff.delete()


        request_status = status.HTTP_204_NO_CONTENT
        return Response(status=request_status)

# END get update and delete staff  ###############################################


# List Event Setting per event ###############################################
class EventSettingByEvent(APIView):
    """Get and create General per event"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        user = request.user
        data = {}
        # check if user is admin return all cards in sys
        # else just the client ones
        eventSettings = None

        eventSettings = getEventSettingsbyEvent(event_id=int(event_id))
        serializer = ListEventSettingsbyEventSerializer(eventSettings, many=True)


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)

    #### No need for post since we create by default once event is created #################################

# END List Event Setting per event per event  ###############################################

class EventSettingByEventDetails(APIView):
    """Get, update and delete event Setting per event """

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]


    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        setting = getEventSettingsbyEventPk(pk=id)
        serializer = ListEventSettingsbyEventSerializer(setting)

        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)




    def patch(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        eventSetting = getEventSettingsbyEventPk(pk=id)
        serializer = ListEventSettingsbyEventSerializer(eventSetting, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)



    def delete(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        staff = getEventSettingsbyEventPk(pk=id)
        staff.delete()


        request_status = status.HTTP_204_NO_CONTENT
        return Response(status=request_status)

# END get update and delete event setting per event  ###############################################