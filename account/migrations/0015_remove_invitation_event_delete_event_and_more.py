# Generated by Django 4.0.2 on 2022-11-23 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_admin_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='event',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Invitation',
        ),
    ]
