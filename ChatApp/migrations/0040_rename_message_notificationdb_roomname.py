# Generated by Django 5.0.6 on 2024-08-23 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0039_rename_roomname_notificationdb_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationdb',
            old_name='message',
            new_name='roomname',
        ),
    ]
