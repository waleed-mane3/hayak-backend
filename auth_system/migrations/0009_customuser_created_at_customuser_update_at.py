# Generated by Django 4.0.2 on 2023-07-14 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0008_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
