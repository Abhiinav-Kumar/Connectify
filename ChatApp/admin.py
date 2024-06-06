from django.contrib import admin
from ChatApp.models import UserDB,Room,Message

# Register your models here.
admin.site.register(UserDB)
admin.site.register(Room)
admin.site.register(Message)
