# Generated by Django 4.0.2 on 2023-03-13 07:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0006_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message="Mobile number must be 10 digits starting with '05'.", regex='^05\\d{8}$')], verbose_name='Mobile Number'),
        ),
    ]
