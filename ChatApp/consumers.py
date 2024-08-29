import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import *
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

import base64
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    
    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room_name=data['room_name'])

        if not Message.objects.filter(message=data['message']).exists():
            new_message = Message(room=get_room_by_name, sender=data['sender'], message=data['message'])
            print("sender :" ,data['sender'])
            print("Message :",data['message'])
            new_message.save()


#private chat settings
class PersonalChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            my_id = self.scope['user'].id
            other_user_id = self.scope['url_route']['kwargs']['id']
            # my_id = 3
            # other_user_id = 1
            # print('Scope:', self.scope)
            # print( 'Current user ',self.scope['user'])
            # print('Another user ',self.scope['url_route'])
            # print("consumer.py : my_id : ", my_id)
            # print("consumer.py : other_user_id : ",other_user_id)


            if int(my_id) > int(other_user_id):
                self.room_name = f'{my_id}-{other_user_id}'
                print('If consumer self.room_name :',self.room_name)

            else:
                self.room_name = f'{other_user_id}-{my_id}'
                print('Else consumer self.room_name :',self.room_name)

            self.room_group_name = 'chat_%s' % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            # Mark notifications as read when the user connects
            # await self.mark_notifications_as_read(my_id, other_user_id, self.room_name)

            await self.accept()

            
        async def receive(self, text_data=None, bytes_data=None):
            data = json.loads(text_data)
            # print(data)
            message = data['message']
            user_id = data['userId']
            receiver_id = data['receiverId']
            image_data = data.get('image', None)

            if image_data:
                image_file = await self.save_image(image_data)
                message = ''
                await self.save_message(user_id, self.room_group_name, message, receiver_id, image_file=image_file)

            else:
                await self.save_message(user_id,self.room_group_name,message,receiver_id)

            await self.save_notification(user_id, receiver_id, self.room_group_name)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message':message,
                    'userId':user_id,
                    'image_url': image_data if image_data else None
                }
            ) 
        
        async def chat_message(self,event):
            message = event['message']
            user_id = event['userId']
            image_url = event.get('image_url', None)

            # print("Chat message function :",message, user_id)


            await self.send(text_data=json.dumps({
                'message':message,
                'userId':user_id,
                'image_url': image_url
            }))


        async def disconnect(self, close_code):
            self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )
            
        @database_sync_to_async
        def save_message(self,sender_id,thread_name,message,receiver_id,image_file=None):
            chat_obj = ChatModelPvt.objects.create(
                sender=sender_id,
                message=message,
                thread_name=thread_name,
                image=image_file)

            return chat_obj
        
        @database_sync_to_async
        def save_notification(self, sender_id, receiver_id, thread_name):
            NotificationDB.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                roomname=thread_name,
                is_read=False  # Initially, the notification is unread
            )

        @database_sync_to_async
        def save_image(self, image_data):
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f'{uuid.uuid4()}.{ext}'
            file_data = ContentFile(base64.b64decode(imgstr), name=file_name)
            return file_data
        
                            



           

       
          