from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ChatApp.models import Room,Message,User_details,NotificationDB


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(User_details)
admin.site.register(NotificationDB)

#private chat 

# @admin.register(MyChats)
# class MyChatsAdmin(admin.ModelAdmin):
#     list_display = ['id','me','frnd','chats']


