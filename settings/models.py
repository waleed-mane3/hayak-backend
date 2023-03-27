from django.db import models
from event.models import Event
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