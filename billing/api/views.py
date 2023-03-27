from django.shortcuts import render
from account.permissions import UserTypeAccessAdminOrClient
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from utils.errors import Error, APIError
from billing.api.queries import (
    getAllCards,
    getClientCards,
    getCardsPk,
    getAllTransactions,
    getClientTransactions,
    getTransaction
    )
from billing.api.serializers import (
    ListCardsSerializer,
    CreateCardsSerializer,
    GetCardsSerializer,
    ListTransactionsSerializer,
    CreateTransactionsSerializer,
    GetTransactionSerializer
    )
from rest_framework import status


# Create your views here.


# List & Create Cards ###############################################
class Cards(APIView):
    """Get and create accounts"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, format=None):
        user = request.user
        data = {}
        cards = None
        # check if user is admin return all cards in sys
        # else just the client ones
        if user.user_type == settings.ADMIN:
            cards = getAllCards()
        else:
            cards = getClientCards(user=user)

        serializer = ListCardsSerializer(cards, many=True)


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)


    def post(self, request, format=None):
        user = request.user
        data = {}
        user_type = None

        serializer = CreateCardsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        request_status = status.HTTP_201_CREATED
        return Response(data=serializer.data, status=request_status)
# END List & Create Cards ###############################################



# List & Create Cards Details ###############################################

class CardsDetails(APIView):
    """Get and create accounts"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        card = getCardsPk(pk=id)
        serializer = ListCardsSerializer(card)

        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)





    def patch(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        card = getCardsPk(pk=id)
        serializer = GetCardsSerializer(card, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)


        # return Response(data=serializer.data, status=request_status)

    def delete(self, request, *args, **kwargs):
        """Delete will not actually delete, but set the custom user to is_active = False"""
        user = request.user
        data = {}
        id = self.kwargs['pk']
        card = getCardsPk(pk=id)
        card.delete()


        request_status = status.HTTP_204_NO_CONTENT
        return Response(status=request_status)

        # return Response(data=serializer.data, status=request_status)
# END List & Create Cards Details ###############################################




# List & Create Transactions ###############################################
class Transactions(APIView):
    """Get and create accounts"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, format=None):
        user = request.user
        data = {}
        transactions = None
        # check if user is admin return all cards in sys
        # else just the client ones
        if user.user_type == settings.ADMIN:
            transactions = getAllTransactions()
        else:
            transactions = getClientTransactions(user=user)

        serializer = ListTransactionsSerializer(transactions, many=True)


        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)



    ####TODO: Transaction and rollback should be applied here #########################################
    # We can use into different ways like,

    # As a decorator
    # from django.db import transaction

    # @transaction.atomic
    # def viewfunc(request):
    # # This code executes inside a transaction.
    # do_stuff()

    # 2) As a context manager

    # from django.db import transaction

    # def viewfunc(request):
    # # This code executes in autocommit mode (Django's default).
    # do_stuff()

    # with transaction.atomic():
    # # This code executes inside a transaction.
    # do_more_stuff()


    def post(self, request, format=None):
        user = request.user
        data = {}
        user_type = None

        serializer = CreateTransactionsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        request_status = status.HTTP_201_CREATED
        return Response(data=serializer.data, status=request_status)


# END List & Create Transactions ###############################################


# List & Create Transactions Details###############################################
class TransactionsDetails(APIView):
    """Get and create accounts"""

    permission_classes = [IsAuthenticated, UserTypeAccessAdminOrClient]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}
        id = self.kwargs['pk']
        transactions = getTransaction(pk=id)
        serializer = GetTransactionSerializer(transactions)

        request_status = status.HTTP_200_OK
        return Response(data=serializer.data, status=request_status)



    # def patch(self, request, *args, **kwargs):
    #     user = request.user
    #     data = {}
    #     id = self.kwargs['pk']
    #     card = getTransaction(pk=id)
    #     serializer = GetTransactionSerializer(card, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()


    #     request_status = status.HTTP_200_OK
    #     return Response(data=serializer.data, status=request_status)

    #     # return Response(data=serializer.data, status=request_status)

    # def delete(self, request, *args, **kwargs):
    #     """Delete will not actually delete, but set the custom user to is_active = False"""
    #     user = request.user
    #     data = {}
    #     id = self.kwargs['pk']

    #     # return Response(data=serializer.data, status=request_status)

# END List & Create Transactions Details ###############################################
