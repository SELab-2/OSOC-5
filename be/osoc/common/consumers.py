"""
websocket consumers are defined here
"""

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class CoachConsumer(WebsocketConsumer):
    """
    CoachConsumer is a consumer linked with the suggestions made by a coach
    """

    def connect(self):
        """
        called when a client connects to the websocket
        """
        async_to_sync(self.channel_layer.group_add)(
            "suggestion",
            self.channel_name
        )

        self.accept()

    def disconnect(self, _):
        """
        called when a client disconnects to the websocket
        """
        async_to_sync(self.channel_layer.group_discard(
            "suggestion",
            self.channel_name
        ))

    def suggestion(self, event):
        """
        a plain suggestion made by a coach
        """
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'suggestion': suggestion
        }))

    def remove_suggestion(self, event):
        """
        when a choach changed the suggestion to: "not decided"
        """
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'remove_suggestion': suggestion
        }))

    def final_decision(self, event):
        """
        a final decision made by an admin
        """
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'final_decision': suggestion
        }))

    def remove_final_decision(self, event):
        """
        when an admin changed the suggestion to: "not decided"
        """
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'remove_final_decision': suggestion
        }))

    def suggest_student(self, event):
        """
        the student is assigned to a project
        """
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'suggest_student': suggestion
        }))

    def remove_student(self, event):
        """
        the student is removed from the project
        """
        suggestion = event['data']

        self.send(text_data=json.dumps({
            'remove_student': suggestion
        }))
