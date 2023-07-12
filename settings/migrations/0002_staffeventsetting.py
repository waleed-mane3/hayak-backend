# Generated by Django 4.0.2 on 2023-03-29 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_dataentry_user_alter_regular_user_and_more'),
        ('event', '0036_invitation_added_by'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffEventSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('staff', models.ManyToManyField(to='account.Client')),
            ],
        ),
    ]