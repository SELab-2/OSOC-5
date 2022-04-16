from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class CoachConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "suggestion",
            self.channel_name
        )

        self.accept()

    def disconnect(self, _):
        async_to_sync(self.channel_layer.group_discard(
            "suggestion",
            self.channel_name
        ))

    def suggestion(self, event):
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'suggestion': suggestion
        }))

    def remove_suggestion(self, event):
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'remove_suggestion': suggestion
        }))

    def final_decision(self, event):
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'final_decision': suggestion
        }))

    def remove_final_decision(self, event):
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'remove_final_decision': suggestion
        }))
