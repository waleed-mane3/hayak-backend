# Generated by Django 4.0.2 on 2022-12-06 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_rename_name_eventtype_name_ar_eventtype_name_en_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(blank=True, max_length=500, null=True)),
                ('title_ar', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
