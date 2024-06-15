import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ChatApp.models import *
from asgiref.sync import async_to_sync


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
            new_message.save()



#private
class PersonalChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            my_id = self.scope['user'].id
            other_user_id = self.scope['url_route']['kwargs']['id']
            if int(my_id) > int(other_user_id):
                self.room_name = f'{my_id}-{other_user_id}'
            else:
                self.room_name = f'{other_user_id}-{my_id}'

            self.room_group_name = 'chat_%s' % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            await self.accept()

        async def disconnect(self, code):
            self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )
            
        async def receive(self, text_data=None, bytes_data=None):
            data = json.loads(text_data)
            message = data['message']
            username = data['username']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message':message,
                    'username':username
                }
            )
        
        async def chat_message(self,event):
            message = event['message']
            username = event['username']

            await self.send(text_data=json.dumps({
                'message':message,
                'username':username
            }))
            