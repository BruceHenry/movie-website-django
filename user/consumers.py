# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'noti_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)

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

    # turn off receive message from websocket

    # # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     print('nhan tin nhan tu websocket 1')
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'message': message,
    #             'type': 'chat_message',
    #         }
    #     )
    #     print('chuyen tin nhan len kenh ')

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print('Nhan tin nhan tu channel room group', message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'chat_message',
        }))
        print('chuyen nguoc lai len websocket')