from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class CoachConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'coach_action',
                'message': message
            }
        )

    def coach_action(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'action',
            'message': message
        }))
