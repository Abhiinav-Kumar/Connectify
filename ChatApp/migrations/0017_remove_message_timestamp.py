# Generated by Django 5.0.6 on 2024-06-17 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0016_message_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='timestamp',
        ),
    ]