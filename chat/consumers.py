import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        sender_name = None
        sender_id = None
        username = self.scope["user"]
        if username:
            sender_name = username.username
            sender_id = username.id

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_name': sender_name,
                'sender_id': sender_id,
            }
        )

    def chat_message(self, event):
        user = self.scope["user"]
        my_name = user.username
        my_id = user.id

        message = event['message']
        sender_name = event['sender_name']
        sender_id = event['sender_id']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'my_name': my_name,
            'my_id': my_id,
            'sender_name': sender_name,
            'sender_id': sender_id,
        }))
