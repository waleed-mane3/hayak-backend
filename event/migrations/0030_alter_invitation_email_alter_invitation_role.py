# Generated by Django 4.0.2 on 2023-02-21 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0029_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='role',
            field=models.CharField(blank=True, choices=[('guest', 'guest'), ('vip', 'vip'), ('management', 'management'), ('participant', 'participant'), ('organizer', 'organizer'), ('media', 'media'), ('instructor', 'instructor')], default='participant', max_length=256, null=True),
        ),
    ]
