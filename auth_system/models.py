from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import _PHONE_REGEX, name_validator
from django.conf import settings



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        (settings.ADMIN, 'Admin'),
        (settings.CLIENT, 'Client')
    )

    username = None
    first_name = models.CharField(_('First Name'), validators=[name_validator], max_length=50, null=True, blank=True)
    last_name = models.CharField(_('Last Name'), validators=[name_validator], max_length=50, null=True, blank=True)
    email = models.EmailField(_('Email Address'), unique=True, blank=False)
    mobile = models.CharField(_('Mobile Number'), validators=[_PHONE_REGEX], max_length=10, null=True, blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=settings.CLIENT)
    image = models.ImageField(upload_to="client_logos", null=True, blank=True)
    first_sign_in = models.BooleanField(default=True)

    # added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    update_at = models.DateTimeField(null=True, auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        self.first_name = self.first_name.strip().lower()
        self.last_name = self.last_name.strip().lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"