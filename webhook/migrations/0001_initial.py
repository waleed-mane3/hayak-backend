# Generated by Django 4.0.2 on 2023-02-18 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcmeWebhookMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(help_text='When we received the event.')),
                ('payload', models.JSONField(default=None, null=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='acmewebhookmessage',
            index=models.Index(fields=['received_at'], name='webhook_acm_receive_70c012_idx'),
        ),
    ]