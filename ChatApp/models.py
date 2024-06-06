from django.db import models

class UserDB(models.Model):

    Email = models.EmailField(max_length=100,null=False,blank=False,unique=True)
    Username = models.CharField(max_length=50,null=True,blank=True,unique=True)
    Password = models.CharField(max_length=50,null=True,blank=True)
    Profile_image = models.ImageField(upload_to="Profile Images",null=True,blank=True)

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

