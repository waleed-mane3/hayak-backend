# Generated by Django 4.0.2 on 2023-02-11 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0025_alter_invitation_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='title',
        ),
    ]
