"""
the signals defined here get notified when certain actions happen in the framework
"""
from django.dispatch import receiver
from django.db.models.signals import pre_save
from osoc.common.models import Coach


@receiver(pre_save, sender=Coach)
def set_new_user_inactive(sender, instance, **kwargs): # pylint: disable=unused-argument
    """
    when creating a new coach set the is_active field to False by default
    """
    if instance._state.adding is True and not instance.is_admin:  # pylint: disable=protected-access
        instance.is_active = False
        