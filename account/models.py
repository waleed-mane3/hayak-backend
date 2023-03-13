from django.db import models
from auth_system.models import CustomUser
import uuid
from django.utils import timezone
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings
from utils.emails import reset_password_email
from event.models import *


## Client Model
class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True) # make sure to archive the deleted user
    field = models.CharField(null=True, blank=True, max_length=256)
    is_assistant = models.BooleanField(default=False)
    is_regular = models.BooleanField(default=False)
    is_scanner = models.BooleanField(default=False)
    is_data_entry = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
## End Client Model


# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True) # make sure to archive the deleted user
    field = models.CharField(null=True, blank=True, max_length=256)

    def __str__(self):
        return self.field
## End Admin Model



# For reset password
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_password_email(
        # token
        reset_password_token.key,
        # name
        f"{reset_password_token.user.first_name} {reset_password_token.user.last_name}",
        # email to:
        reset_password_token.user.email
    )






## Scanner Model
class Scanner(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True) # make sure to archive the deleted user
    events = models.ManyToManyField(Event, null=True, related_name='scanners')

    def __str__(self):
        return f"{self.user.user.first_name} {self.user.user.last_name}"
## End Scanner


## Regular Model
class Regular(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True) # make sure to archive the deleted user

    def __str__(self):
        return f"{self.user.user.first_name} {self.user.user.last_name}"
## End Regular

## Regular Model
class DataEntry(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True) # make sure to archive the deleted user
    events = models.ManyToManyField(Event, null=True, related_name='dataEntry')

    def __str__(self):
        return f"{self.user.user.first_name} {self.user.user.last_name}"
## End Regular

















# # create profiles when update user
# @receiver(post_save, sender=CustomUser)
# def create_user_role(sender, instance, created, **kwargs):
#     if created:
#         if instance.user_type == 1:
#             Admin.objects.create(user=instance)

#         if instance.user_type == 2:
#             Client.objects.create(user=instance)


# # update profiles when update user
# @receiver(post_save, sender=CustomUser)
# def save_user_role(sender, instance, **kwargs):

#     if instance.user_type == 1:
#         instance.admin.save()

#     if instance.user_type == 2:
#         instance.client.save()




