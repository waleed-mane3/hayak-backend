from rest_framework import serializers
from billing.models import *


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = '__all__'




class ListCardsSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer()
    class Meta:
        model = Cards
        fields = '__all__'
        extra_kwargs = {
            'number': {'write_only': True},
            'cvv': {'write_only': True}
        }


class CreateCardsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cards
        fields = '__all__'
        extra_kwargs = {
            'number': {'write_only': True},
            'cvv': {'write_only': True},
            'user': {'required': False}
        }

    def save(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        card = Cards(
            user = user,
            name = self.validated_data['name'],
            number = self.validated_data['number'],
            expiry_date = self.validated_data['expiry_date'],
            cvv = self.validated_data['cvv'],
            payment_method = self.validated_data['payment_method']
        )
        card.save()

        return card

class GetCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'
        extra_kwargs = {
            'number': {'write_only': True, 'required': False},
            'cvv': {'write_only': True, 'required': False},
            'user': {'required': False}
        }

class ListTransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = '__all__'

class CreateTransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }

    def save(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        trans = Transactions(
            user = user,
            status = self.validated_data['status'],
            paid_at = self.validated_data['paid_at'],
            total_price = self.validated_data['total_price'],
            product = self.validated_data['product'],
            quantity = self.validated_data['quantity'],
            subtotal = self.validated_data['subtotal'],
            discunt = self.validated_data['discunt'],
            tax = self.validated_data['tax']
        )
        trans.save()

        return trans


class GetTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
