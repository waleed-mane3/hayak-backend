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


