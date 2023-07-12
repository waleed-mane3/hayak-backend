# Generated by Django 4.0.2 on 2023-03-27 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0036_invitation_added_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration', models.BooleanField(default=False)),
                ('communication_method', models.PositiveSmallIntegerField(choices=[(1, 'Email'), (2, 'whatsapp'), (3, 'SMS')], default=1)),
                ('language', models.PositiveSmallIntegerField(choices=[(1, 'English'), (2, 'Arabic')], default=1)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
    ]