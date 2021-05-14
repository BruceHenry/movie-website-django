# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'group1'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('nhan tin nhan tu websocket 1')
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print('chuyen tin nhan len kenh ')

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print('Nhan tin nhan tu channel room group', message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))
        print('chuyen nguoc lai len websocket')