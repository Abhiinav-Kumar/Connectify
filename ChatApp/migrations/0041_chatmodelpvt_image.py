# Generated by Django 5.0.6 on 2024-08-29 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0040_rename_message_notificationdb_roomname'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodelpvt',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images/'),
        ),
    ]
