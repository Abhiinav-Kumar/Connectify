# Generated by Django 5.0.6 on 2024-06-02 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=100, unique=True)),
                ('Username', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('Password', models.CharField(blank=True, max_length=50, null=True)),
                ('Profile_image', models.ImageField(blank=True, null=True, upload_to='Profile_Images')),
                ('Date_joined', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
