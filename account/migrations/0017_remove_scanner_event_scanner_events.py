# Generated by Django 4.0.2 on 2023-03-02 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0034_invitation_entries_invitation_invitation_type'),
        ('account', '0016_scanner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanner',
            name='event',
        ),
        migrations.AddField(
            model_name='scanner',
            name='events',
            field=models.ManyToManyField(null=True, to='event.Event'),
        ),
    ]
