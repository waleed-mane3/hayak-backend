# Generated by Django 4.0.2 on 2023-02-23 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0031_alter_invitation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='email_sent',
            field=models.BooleanField(default=False, verbose_name='Email Sent'),
        ),
    ]