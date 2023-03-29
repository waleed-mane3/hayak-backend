from rest_framework import serializers
from settings.models import *
from account.models import Client, CustomUser


class ListGeneralSerializer(serializers.ModelSerializer):

    class Meta:
        model = General
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class CustomClientStaffSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    client_id = serializers.SerializerMethodField()

    def get_client_id(self, obj):
        return obj.pk

    class Meta:
        model = Client
        fields = '__all__'


class ListStaffSettingsSerializer(serializers.ModelSerializer):
    staff = CustomClientStaffSerializer(many=True)
    class Meta:
        model = StaffEventSetting
        fields = '__all__'
        extra_kwargs = {
            'event': {'write_only': True, 'required': True},
        }
