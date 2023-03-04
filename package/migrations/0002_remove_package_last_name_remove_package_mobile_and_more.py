# Generated by Django 4.0.2 on 2022-12-13 19:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='package',
            name='mobile',
        ),
        migrations.AddField(
            model_name='package',
            name='features',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), blank=True, default=[], null=True, size=None),
        ),
        migrations.AddField(
            model_name='package',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]