# Generated by Django 5.0.6 on 2024-08-22 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0033_alter_notificationdb_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationdb',
            name='message',
        ),
        migrations.AddField(
            model_name='notificationdb',
            name='roomname',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notificationdb',
            name='threadname',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
