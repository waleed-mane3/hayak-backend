# Generated by Django 4.0.2 on 2023-01-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0018_invitation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
