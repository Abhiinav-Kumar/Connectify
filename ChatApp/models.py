from django.db import models
from django.contrib.auth.models import User



#public chat room model
class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name

    def return_room_messages(self):
        return Message.objects.filter(room=self)

    def create_new_room_message(self, sender, message):
        new_message = Message(room=self, sender=sender, message=message)
        new_message.save()


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    

    def __str__(self):
        return str(self.room)
    

# Private chat
class ChatModelPvt(models.Model):
    sender = models.IntegerField( default=None)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.message

 
    
# User details model
class User_details(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,default=0)
    user_name = models.CharField(max_length=150, unique=True)
    profile_image = models.ImageField(upload_to="Profile_Images",null=True,blank=True,default="logo/default.png")
    Bio = models.CharField(max_length=50,null=True,blank=True,default="Connectify")

    # def __str__(self):
    #     return self.user_name

    # def get_user(self):
    #     return User.objects.get(username=self.user_name)


class NotificationDB(models.Model):
    sender = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='sender_notification',null=True,blank=True)
    receiver = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='receiver_notification',null=True,blank=True)
    roomname = models.CharField(max_length=100,null=True,blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)   
    





    
   

    