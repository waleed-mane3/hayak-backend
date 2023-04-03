from django.db import models
from event.models import Event
from account.models import Client
# Create your models here.


class General(models.Model):
    COMMUNICATION_TYPE_CHOICES = (
        (1, 'Email'),
        (2, 'whatsapp'),
        (3, 'SMS'),
    )
    LANGUAGE_TYPE_CHOICES = (
        (1, 'English'),
        (2, 'Arabic'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE) # make sure to archive the deleted user
    registration = models.BooleanField(default=False)
    communication_method = models.PositiveSmallIntegerField(choices=COMMUNICATION_TYPE_CHOICES, default=1)
    language = models.PositiveSmallIntegerField(choices=LANGUAGE_TYPE_CHOICES, default=1)


    def __str__(self):
        return f"{self.event.name}-{self.event.id}"

class StaffEventSetting(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE) # make sure to archive the deleted user
    staff = models.ManyToManyField(Client)


    def __str__(self):
        return f"{self.event.name}-{self.event.id}"


class Zones(models.Model):
    name = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"{self.name}"
class TicketType(models.Model):
    name = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"{self.name}"


class EventSetting(models.Model):
    ENTERIES_PER_QR = (
        (1, 'Single entry'),
        (2, 'Multiple entries'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE) # make sure to archive the deleted user
    multiple_tickets_per_qr = models.BooleanField(default=True)
    entries_per_qr = models.PositiveSmallIntegerField(choices=ENTERIES_PER_QR, default=1)
    zones = models.ManyToManyField(Zones) # make sure to archive the deleted user
    ticket_type = models.ManyToManyField(TicketType) # make sure to archive the deleted user




    def __str__(self):
        return f"{self.event.name}-{self.event.id}"