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
        studentId = text_data_json['studentId']
        coachId = text_data_json['coachId']
        suggestion = text_data_json['suggestion']
        reason = text_data_json['reason']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'coach_action',
                'studentId': studentId,
                'coachId': coachId,
                'suggestion': suggestion,
                'reason': reason
            }
        )

    def coach_action(self, event):
        studentId = event['studentId']
        coachId = event['coachId']
        suggestion = event['suggestion']
        reason = event['reason']

        self.send(text_data=json.dumps({
            'type': 'coach_action',
            'studentId': studentId,
            'coachId': coachId,
            'suggestion': suggestion,
            'reason': reason
        }))
