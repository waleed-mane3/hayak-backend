from rest_framework.serializers import ModelSerializer
from package.models import Package


class PackageSerializer(ModelSerializer):

    class Meta:
        model = Package
        fields = '__all__'






# 15 people, Use Hayak website to send your invitations, Send via email only, Attendance Confirmation, Barcode for each person, Ready-made design of your choice, Using the Hayak Scanning App
# Use Hayak website to send your invitations, Send via WhatsApp, email and SMS, Attendance Confirmation, Barcode for each person, Event site, Using the Hayak Scanning App
# 100 people, Completely manage your invitation, All features of the basic package, Manage and send invitations on your behalf, Employee for organizing the entry, Complete customer service, Ready-made design of your choice
# 200 people, Completely manage your invitation, All features of the basic package, Manage and send invitations on your behalf, Employee for organizing the entry, Complete customer service, Ready-made design of your choice
# 500 people, Completely manage your invitation, All features of the basic package, Manage and send invitations on your behalf, Employee for organizing the entry, Complete customer service, Ready-made design of your choice or special design
