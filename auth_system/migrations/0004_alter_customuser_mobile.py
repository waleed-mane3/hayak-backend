# Generated by Django 4.0.2 on 2022-11-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0003_remove_customuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Mobile Number'),
        ),
    ]
