from billing.models import *
from utils.errors import Error, APIError


def getAllCards():
    try:
        return Cards.objects.all()
    except Cards.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Cards._meta.model_name])


def getClientCards(user):
    try:
        return Cards.objects.filter(user=user)
    except Cards.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Cards._meta.model_name])

def getCardsPk(pk):
    try:
        return Cards.objects.get(id=pk)
    except Cards.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Cards._meta.model_name])


def getAllTransactions():
    try:
        return Transactions.objects.all()
    except Transactions.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Transactions._meta.model_name])

def getClientTransactions(user):
    try:
        return Transactions.objects.filter(user=user)
    except Transactions.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Transactions._meta.model_name])

def getTransaction(pk):
    try:
        return Transactions.objects.get(id=pk)
    except Transactions.DoesNotExist as er:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Transactions._meta.model_name])