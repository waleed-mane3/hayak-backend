from auth_system.models import CustomUser
from account.models import Scanner
from event.models import Event
from utils.errors import Error, APIError
from django.db.models import Q
from typing import Iterable





def getAllCustomUser():
    try:
        return CustomUser.objects.all(is_active=True)
    except CustomUser.DoesNotExist as er:
        print('sadkljfghkasjdfhlk')


def getCustomUser(pk):
    try:
        return CustomUser.objects.get(id=pk, is_active=True)
    except CustomUser.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[CustomUser._meta.model_name])



def getClientUsersAndRelated(user: CustomUser) -> Iterable[CustomUser]:
    """Get Client all events
        - Retrive all events by user
        - Get all Staff users by events's id related to
            - Staff (Scanner ...etc)
        - Get all Custom user by id collected...


        TODO: Any new added User type should include here
    """
    try:
        userIds = []
        events = Event.objects.filter(user=user)
        userIds.append(user.id)

        ## Filter for M2M field by event id in Scanner Models
        staffScanner = Scanner.objects.filter(events__id__in=events).values_list('user', flat=True)

        userIds = userIds + list(staffScanner)
        users = CustomUser.objects.filter(Q(id__in=userIds), Q(is_active=True))
        return users

    except Exception as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[str(er)])