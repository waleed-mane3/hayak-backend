from django.db import models
from auth_system.models import CustomUser
from utils.validators import _CARD_HOLDER_NAME_REGEX
import uuid


# Create your models here.
class Transactions(models.Model):

    STATUS_CHOICES = (
        (1, 'Paid'),
        (2, 'Cancelled'),
        (3, 'Unpaid'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING) # make sure to archive the deleted user
    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    paid_at = models.DateTimeField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    product = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)
    discunt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

#TODO: Shell we or not saving the client cards details ??
class Cards(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING) # make sure to archive the deleted user
    name = models.CharField(blank=False, validators=[_CARD_HOLDER_NAME_REGEX], max_length=255)
    number = models.IntegerField(blank=False)
    expiry_date = models.DateField()
    cvv = models.IntegerField(blank=False)
    payment_method= models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


