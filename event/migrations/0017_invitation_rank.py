# Generated by Django 4.0.2 on 2023-01-25 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0016_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='rank',
            field=models.CharField(choices=[('participant', 'participant'), ('guest', 'guest'), ('backyard', 'backyard'), ('vip', 'vip')], default='participant', max_length=256),
        ),
    ]
