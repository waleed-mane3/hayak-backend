from django.db import models
from auth_system.models import CustomUser
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime
from django.utils.translation import gettext_lazy as _
# generate qr 
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
import time
from django.core.files import File
from utils.emails import invitation_email



def email_history():
    history = {
        "pending": False,
        "confirmed": False,
        "attended": False,
        "cancelled": False
    }
    return history



# Event Types ##########################################################
class EventType(models.Model):
    # value = models.AutoField(primary_key=True)
    label = models.CharField(max_length=500, null=True, blank=True)
    label_ar = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.label
########################################################################



# Invitation Status #################################################### 
class InvitationStatus(models.Model):
    # value = models.AutoField(primary_key=True)
    label = models.CharField(max_length=500, null=True, blank=True)
    label_ar = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.label
########################################################################



# Cities ###############################################################
class City(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
########################################################################

# from datetime import datetime
# def validate_event_date(value):
#     current_date = datetime.now()
#     if value < current_date:
#         raise ValidationError(_('Choose today date or later!'), params={'value': value},)

#
# Events ###############################################################
class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="events")
    name = models.CharField(max_length=500, blank=True, null=True, default="none")
    type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, related_name="event_types")
    venue = models.CharField(max_length=500, blank=True, null=True, default="none")
    location = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True, default="Saudi Arabia")
    date = models.DateTimeField(default=timezone.now)

    # review these
    capacity = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="events", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # this date will never be updated
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    # this date will change every time we update entry
    update_at = models.DateTimeField(null=True, auto_now=True)


    def __str__(self):
        return self.name
##########################################################################



# People Titles ##########################################################
class Title(models.Model):
    title_en = models.CharField(max_length=500, null=True, blank=True)
    title_ar = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.title_en
##########################################################################



# Rank ##########################################################
class Rank(models.Model):
    name_en = models.CharField(max_length=500, null=True, blank=True)
    name_ar = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name_en
##########################################################################



# Invitations #############################################################
class Invitation(models.Model):
    ROLE_CHOICES = (
        ('guest', 'guest'),
        ('vip', 'vip'),
        ('management', 'management'),
        ('participant', 'participant'),
        ('organizer', 'organizer'),
        ('media', 'media'),
        ('instructor', 'instructor'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    # title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
    # title = models.CharField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    mobile = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    entries = models.IntegerField(default=1)
    invitation_type = models.CharField(max_length=1000, null=True, blank=True, default="no type")
    role = models.CharField(default="participant", max_length=256, choices=ROLE_CHOICES, null=True, blank=True)
    status = models.ForeignKey(InvitationStatus, on_delete=models.CASCADE, null=True, default=2)
    reference = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    is_generated = models.BooleanField(verbose_name=_("Invitation Generated"), default=False)
    email_sent = models.BooleanField(verbose_name=_("Email Sent"), default=False)
    qr_url = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="invitations", null=True, blank=True)
    qr = models.ImageField(upload_to="qrs", null=True, blank=True)
    invitation = models.ImageField(upload_to="invitations", null=True, blank=True)


    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # email_history = models.JSONField(default=email_history)
    # this date will never be updated
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    # this date will change every time we update entry
    update_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
###########################################################################


# # after create invitation create the qr code image and save it for this user
# @receiver(post_save, sender=Invitation)
# def save_id_inside_qr(sender, instance, created, **kwargs):
    
#     if created: 
#         if instance.id:
#             qr_image = qrcode.make(instance.id)
#             qr_offset = Image.new('RGB', (290, 290), 'white')
#             draw_img = ImageDraw.Draw(qr_offset)
#             qr_offset.paste(qr_image)
#             file_name = f'{instance.name}-{instance.id}-{str(time.time())}.png'
#             stream = BytesIO()
#             qr_offset.save(stream, 'PNG')
#             instance.qr_code.save(file_name, File(stream), save=False)
#             qr_offset.close()
#             instance.save()
            

#         # send email 
#         invitation_email(
#             instance.name,
#             instance.email,
#             instance.event.name,
#             instance.event.date,
#             instance.event.location,
#             instance.qr_code.url
#         )



# Generate qr #############################################################
@receiver(post_save, sender=Invitation)
def save_id_inside_qr(sender, instance, created, **kwargs):
    
    if created: 
        # if instance.id:
        #     # qr_image = qrcode.make(instance.id)

        #     qr = qrcode.QRCode(
        #         version=1,
        #         error_correction=qrcode.constants.ERROR_CORRECT_L,
        #         box_size=10,
        #         border=4,
        #     )
        #     qr.add_data(instance.reference)
        #     qr.make(fit=True)
        #     qr_image = qr.make_image(fill_color="#0f2738", back_color="white")

        #     qr_offset = Image.new('RGBA', (370, 370), (255, 0, 0, 0))
        #     draw_img = ImageDraw.Draw(qr_offset)
        #     qr_offset.paste(qr_image)
        #     # file_name = f'{instance.first_name}-{instance.last_name}-{instance.id}-{str(time.time())}.png'
        #     file_name = f'{instance.first_name}-{instance.last_name}-{instance.reference}.png'
        #     stream = BytesIO()
        #     # https://stackoverflow.com/questions/8376359/how-to-create-a-transparent-gif-or-png-with-pil-python-imaging
        #     qr_offset.save(stream, 'GIF', transparency=1)
        #     instance.qr.save(file_name, File(stream), save=False)
        #     qr_offset.close()
        #     instance.save()

        if instance.id:
            qr_image = qrcode.make(instance.reference)
            qr_offset = Image.new('RGB', (370, 370), 'white')
            draw_img = ImageDraw.Draw(qr_offset)
            qr_offset.paste(qr_image)
            file_name = f'{instance.first_name}-{instance.last_name}-{instance.entries}-{instance.mobile}-{str(time.time())}.png'
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            instance.qr.save(file_name, File(stream), save=False)
            qr_offset.close()
            instance.save()

            # # send email 
            # invitation_email(
            #     f"{instance.first_name} {instance.last_name}",
            #     instance.email,
            #     instance.event.name,
            #     str(instance.event.date.date()),
            #     instance.event.location,
            #     instance.qr.url,
            #     instance.event.venue,
            #     instance.event.city
            # )
###########################################################################


















##############################################
class Checkin(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)

    # this date will never be updated
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    # this date will change every time we update entry
    update_at = models.DateTimeField(null=True, auto_now=True)

    FilterFields = ['date']
##################################################




class Order(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name
##################################################