# Generated by Django 4.0.2 on 2023-03-08 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0034_invitation_entries_invitation_invitation_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitation',
            old_name='entries',
            new_name='tickets',
        ),
    ]
