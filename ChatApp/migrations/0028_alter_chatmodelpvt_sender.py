# Generated by Django 5.0.6 on 2024-06-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0027_alter_user_details_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmodelpvt',
            name='sender',
            field=models.IntegerField(default=None),
        ),
    ]