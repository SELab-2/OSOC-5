#!/usr/bin/env python
if __name__ == "__main__":
    """ This stuff allows to import modules & sets Django settings. """
    from os import sys, path, environ
    from django.core.management import call_command

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    environ.setdefault("DJANGO_SETTINGS_MODULE", "osoc.settings.dev")

    import django
    django.setup()

    from osoc.common.models import Coach
    from django.core.exceptions import ObjectDoesNotExist

    try:
        Coach.objects.get(email='admin@example.com')
    except ObjectDoesNotExist:
        Coach.objects.create_superuser(
            first_name='admin', last_name='admin', password='dev', email='admin@example.com', is_admin=True)
