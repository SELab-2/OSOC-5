"""
the websocket-specific urls are defined here
"""

from django.urls import path
from .consumers import CoachConsumer

ws_urlpatterns = [
    path('ws/socket_server/', CoachConsumer.as_asgi())
]
