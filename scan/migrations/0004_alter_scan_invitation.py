# Generated by Django 4.0.2 on 2023-03-10 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0036_invitation_added_by'),
        ('scan', '0003_scan_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='invitation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.invitation'),
        ),
    ]