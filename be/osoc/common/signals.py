from django.dispatch import receiver
from django.db.models.signals import pre_save

from osoc.common.models import Coach, Student


@receiver(pre_save, sender=Coach)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.is_active = False


@receiver(pre_save, sender=Student)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.is_active = False
