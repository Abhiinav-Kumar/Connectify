# Generated by Django 5.0.6 on 2024-06-04 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdb',
            name='Date_joined',
        ),
        migrations.RemoveField(
            model_name='userdb',
            name='Profile_image',
        ),
        migrations.AlterField(
            model_name='userdb',
            name='Password',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
