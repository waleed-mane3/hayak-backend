from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField



class Package(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    features = ArrayField(models.CharField(max_length=1000), blank=True, null=True, default=[])

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name

