#!/usr/bin/env python
if __name__ == "__main__":
    """ This stuff allows to import modules & sets Django settings. """
    from os import sys, path, environ
    from django.core.management import call_command

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    environ.setdefault("DJANGO_SETTINGS_MODULE", "osoc.settings")

    import django
    django.setup()

    from django.contrib.auth.models import User
    from django.core.exceptions import ObjectDoesNotExist

    try:
        User.objects.get(username='admin')
    except ObjectDoesNotExist:
        User.objects.create_superuser('admin', 'admin@example.com', 'dev')

