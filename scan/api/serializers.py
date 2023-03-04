from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from scan.models import Scan



class ScanSerializer(ModelSerializer):

    class Meta:
        model = Scan
        fields = '__all__'
        depth=1


