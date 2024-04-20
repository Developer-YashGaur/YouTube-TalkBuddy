import json
from tokenize import TokenError
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            try:
                token = headers[b'authorization'].decode().split()[1]
                validated_token = JWTAuthentication().get_validated_token(token)
                user_id = validated_token['user_id']
                user1 = await database_sync_to_async(User.objects.get)(id = user_id)
                self.scope['user'] = user1
                room_id = self.scope['url_route']['kwargs']['room_id']
                receiver_user = room_id.split('_', 1)[1]
                receiver_user = PhoneNumber.from_string(receiver_user)
                user2 = await database_sync_to_async(User.objects.get)(mobileNumber=receiver_user.as_e164)
                room = await database_sync_to_async(ChatRoom.find_or_create)(user1, user2)
                # print(room.id, user1.mobileNumber, user2.mobileNumber)
                self.room_group_name = f'chat_{room.id}'
                # self.room_group_name = room_id
                self.user = self.scope.get('user')
                print(self.channel_name, self.room_group_name)
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            
            except InvalidToken:
                await self.close()
                return
        else:
            await self.close()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(message, self.room_group_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message}
        )

    @database_sync_to_async
    def save_message(self, message, room_name):
        room = ChatRoom.objects.get(id=room_name.split('_')[1])
        Message.objects.create(chat_room=room, text=message, sender=self.scope['user'])

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    
