from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ChatApp.models import Room,Message




admin.site.register(Room)
admin.site.register(Message)

