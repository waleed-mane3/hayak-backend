# Generated by Django 4.0.2 on 2022-12-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_title_title_ar_title_title_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='country',
            field=models.CharField(blank=True, default='Saudi Arabia', max_length=500, null=True),
        ),
    ]
