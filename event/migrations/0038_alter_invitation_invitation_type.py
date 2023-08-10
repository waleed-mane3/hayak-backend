# Generated by Django 4.0.2 on 2023-07-14 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0037_invitationtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invitation_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invitation_types', to='event.invitationtype'),
        ),
    ]
