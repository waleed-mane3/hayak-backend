from django.db import models
from django.utils import timezone
import uuid
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from event.models import Event, Invitation
from auth_system.models import CustomUser

class Scan(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    scanned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)

    # this date will never be updated
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    # this date will change every time we update entry
    update_at = models.DateTimeField(null=True, auto_now=True)

    # FilterFields = ['date']