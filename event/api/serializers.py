from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from event.models import Event, Invitation, EventType, InvitationStatus


class EventsSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'name', 'capacity', 'is_active']
        read_only_fields = ['user']





class EventSerializer(ModelSerializer):

    total = serializers.SerializerMethodField('totals')
    confirmed = serializers.SerializerMethodField('confirmeds')
    attended = serializers.SerializerMethodField('attendeds')
    pending = serializers.SerializerMethodField('pendings')
    cancelled = serializers.SerializerMethodField('cancelleds')

    type = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['user']


    def totals(self, Event):
        totals = Event.invitation_set.all()
        return totals.count()
    
    def pendings(self, Event):
        pendings = Event.invitation_set.filter(status=1)
        return pendings.count()

    def confirmeds(self, Event):
        confirmeds = Event.invitation_set.filter(status=2)
        return confirmeds.count()
    
    def attendeds(self, Event):
        attendeds = Event.invitation_set.filter(status=3)
        return attendeds.count()
    
    
    def cancelleds(self, Event):
        cancelleds = Event.invitation_set.filter(status=4)
        return cancelleds.count()



# Update Event Serializer 
class UpdateEventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['user']


    

class InvitationSerializer(ModelSerializer):
    status = serializers.StringRelatedField()
    used_tickets = serializers.SerializerMethodField("used_tickets_function")
    added_by = serializers.SerializerMethodField("added_by_function")

    class Meta:
        model = Invitation
        exclude = ('role',)
    
    # def guest_email(self, obj):
    #     email = obj.email
    #     return email.lower()

    def used_tickets_function(self, obj):
        tickets_count = obj.scan_set.all().count()
        return tickets_count
    
    def added_by_function(self, obj):
        added_by = f"{obj.first_name} {obj.last_name}"
        return added_by


    

class UpdateInvitationSerializer(ModelSerializer):

    class Meta:
        model = Invitation
        fields = '__all__'




class EventTypeSerializer(ModelSerializer):

    class Meta:
        model = EventType
        fields = ('id', 'label',)


class InvitationStatusSerializer(ModelSerializer):

    class Meta:
        model = InvitationStatus
        fields = ('id', 'label',)



class CreateEventSerializer(ModelSerializer):
    class Meta:

        model = Event
        fields = '__all__'
        read_only_fields = ['user']



# class UpdateEventSerializer(ModelSerializer):
#     class Meta:

#         model = Event
#         fields = ['name', 'venue', 'location', 'city', 'country', 'date']



class UserEventsSerializer(ModelSerializer):

    no_invitations = serializers.SerializerMethodField('number_of_invitations')
    pending = serializers.SerializerMethodField('pendings')
    waiting = serializers.SerializerMethodField('waitings')
    confirmed = serializers.SerializerMethodField('confirmeds')
    accepted = serializers.SerializerMethodField('accepteds')
    canceled = serializers.SerializerMethodField('canceleds')
    checked = serializers.SerializerMethodField('checkeds')

    class Meta:
        model = Event
        fields = ['id', 'user', 'name', 'venue', 'location', 'city', 'country', 'date', 'capacity', 'no_invitations','image', 'pending', 'waiting', 'confirmed', 'accepted', 'canceled', 'checked']
    
    def number_of_invitations(self, Event):
        invitations = Event.invitation_set.all()
        return invitations.count()
    
    
    def pendings(self, Event):
        pending = Event.invitation_set.filter(status="pending")
        return pending.count()

    def waitings(self, Event):
        waiting = Event.invitation_set.filter(status="waiting")
        return waiting.count()
    
    def confirmeds(self, Event):
        confirmed = Event.invitation_set.filter(status="confirmed")
        return confirmed.count()
    
    def accepteds(self, Event):
        accepted = Event.invitation_set.filter(status="accepted")
        return accepted.count()
    
    def canceleds(self, Event):
        canceled = Event.invitation_set.filter(status="apologized")
        return canceled.count()

    def checkeds(self, Event):
        checked = Event.invitation_set.filter(status="checked")
        return checked.count()
    
    

class CreateInvitationSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ['id', 'event', 'first_name', 'last_name', 'mobile', 'email', 'status']
        read_only_fields = ['event']


class InvitationUrlSerializer(ModelSerializer):
    class Meta:

        model = Invitation
        fields = ["image"]


# class GetCheckinsSerializer(ModelSerializer):
#     class Meta:

#         model = Checkin
#         fields = ['invitation', 'date' , 'time']
#         depth = 1


# class CreateCheckinSerializer(ModelSerializer):
#     class Meta:

#         model = Checkin
#         fields = ['invitation']

        

# Get General Statistics
class GetGeneralStatisticsSerializer(serializers.Serializer):
    pending = serializers.IntegerField()
    



# Get all invitation for one event 
class EventInvitationsSerializer(ModelSerializer):

    class Meta:
        model = Invitation
        fields = ['id', 'event', 'first_name', 'last_name', 'mobile', 'email', 'status']