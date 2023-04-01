from rest_framework import serializers
from settings.models import *
from account.models import Client, CustomUser
from django.db import transaction


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


class ZonesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zones
        fields = '__all__'

class TicketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketType
        fields = '__all__'

class ListEventSettingsbyEventSerializer(serializers.ModelSerializer):
    zones = ZonesSerializer(many=True)
    ticket_type = TicketTypeSerializer(many=True)



    class Meta:
        model = EventSetting
        fields = '__all__'


    ## Rollback all changes if not all successful updated
    @transaction.atomic
    def update(self, instance, validated_data):
        zones_list = self.initial_data.get('zones')
        ticket_type_list = self.initial_data.get('ticket_type')
        multiple_tickets_per_qr = self.initial_data.get('multiple_tickets_per_qr')
        entries_per_qr = self.initial_data.get('entries_per_qr')
        instance.multiple_tickets_per_qr = multiple_tickets_per_qr
        instance.entries_per_qr = entries_per_qr


        if zones_list:
            ### Clear the field from all inctances
            instance.zones.clear()
            for i in zones_list:
                zone_id = i.get('id')
                if zone_id:
                    ## get the exsited one
                    zone = Zones.objects.get(pk=zone_id)
                    ### Update the name if so
                    zone.name = i.get('name')
                    zone.save()
                    instance.zones.add(zone)
                else:
                    # create new one and add it to the perant instance
                    zone = Zones.objects.create(
                            name=i.get('name')
                        )
                    instance.zones.add(zone)

        if ticket_type_list:
            ### Clear the field from all inctances
            instance.ticket_type.clear()
            for i in ticket_type_list:
                ticket_type_id = i.get('id')
                if ticket_type_id:
                    ## get the exsited one
                    ticket_type = TicketType.objects.get(pk=ticket_type_id)
                    ### Update the name if so
                    ticket_type.name = i.get('name')
                    ticket_type.save()
                    instance.ticket_type.add(ticket_type)
                else:
                    # create new one and add it to the perant instance
                    ticket_type = TicketType.objects.create(
                            name=i.get('name')
                        )
                    instance.ticket_type.add(ticket_type)



        instance.save()
        return instance
