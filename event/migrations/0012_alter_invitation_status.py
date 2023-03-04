# Generated by Django 4.0.2 on 2022-12-23 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_rename_name_en_eventtype_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('confirmed', 'confirmed'), ('attended', 'attended'), ('cancelled', 'cancelled')], default='pending', max_length=300),
        ),
    ]