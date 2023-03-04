# Generated by Django 4.0.2 on 2023-01-28 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0022_alter_invitation_email_alter_invitation_status'),
        ('scan', '0002_remove_scan_event_scan_scanned_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.event'),
        ),
    ]
