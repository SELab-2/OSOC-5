"""
Application definitions.
"""
from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    set a name and other fields for this app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'osoc.common'

    def ready(self):
        import osoc.common.signals
