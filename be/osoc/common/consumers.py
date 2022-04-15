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
        # def coach_action(self, event):
        studentId = event['studentId']
        coachId = event['coachId']
        suggestion = event['suggestion']
        reason = event['reason']

        self.send(text_data=json.dumps({
            'type': 'final_decision',
            'studentId': studentId,
            'coachId': coachId,
            'suggestion': suggestion,
            'reason': reason
        }))
