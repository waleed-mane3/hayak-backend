# Generated by Django 4.0.2 on 2023-07-22 16:11

import django.core.validators
from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0009_customuser_created_at_customuser_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[utils.validators.name_validator], verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[utils.validators.name_validator], verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message="Mobile number must be 10 digits starting with '05'.", regex='^05\\d{8}$')], verbose_name='Mobile Number'),
        ),
    ]
