# Generated by Django 4.0.2 on 2022-12-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_invitation_first_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventtype',
            old_name='name',
            new_name='name_ar',
        ),
        migrations.AddField(
            model_name='eventtype',
            name='name_en',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='nickname',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]