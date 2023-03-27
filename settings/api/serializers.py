from rest_framework import serializers
from settings.models import *


class ListGeneralSerializer(serializers.ModelSerializer):

    class Meta:
        model = General
        fields = '__all__'
