# Generated by Django 4.0.2 on 2022-03-10 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='mobile',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
