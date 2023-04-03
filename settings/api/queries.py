from settings.models import *
from utils.errors import Error, APIError
from event.models import Event


def getAllGeneral():
    try:
        return General.objects.all()
    except General.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[General._meta.model_name])

def getEvent(event_id):
    try:
        return Event.objects.get(id=event_id)
    except Event.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Event._meta.model_name])


def getEventGeneralSettings(event_id):
    try:
        event = getEvent(event_id=event_id)
        return General.objects.filter(event=event)
    except General.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[General._meta.model_name])


def getGeneralPk(pk):
    try:
        return General.objects.get(id=pk)
    except General.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[General._meta.model_name])



def getEventStaffSettings(event_id):
    try:
        event = getEvent(event_id=event_id)
        return StaffEventSetting.objects.filter(event=event)
    except StaffEventSetting.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[StaffEventSetting._meta.model_name])


def getEventStaffSettingsPk(pk):
    try:
        return StaffEventSetting.objects.get(id=pk)
    except StaffEventSetting.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[StaffEventSetting._meta.model_name])



def getEventSettingsbyEvent(event_id):
    try:
        event = getEvent(event_id=event_id)
        return EventSetting.objects.filter(event=event)
    except EventSetting.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[EventSetting._meta.model_name])


def getEventSettingsbyEventPk(pk):
    try:
        return EventSetting.objects.get(id=pk)
    except EventSetting.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[EventSetting._meta.model_name])

