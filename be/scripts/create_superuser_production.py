#!/usr/bin/env python
if __name__ == "__main__":
    """ This stuff allows to import modules & sets Django settings. """
    from os import sys, path, environ
    from django.core.management import call_command

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    environ.setdefault("DJANGO_SETTINGS_MODULE", "osoc.settings.prod")

    import django
    django.setup()

    from osoc.common.models import Coach
    from django.core.exceptions import ObjectDoesNotExist

    # Admin
    try:
        Coach.objects.get(email='selah@sudo.com')
    except ObjectDoesNotExist:
        Coach.objects.create_superuser(first_name='Selah', last_name='Sudo', is_admin=True,
                                       email='selah@sudo.com', password=environ['DJANGO_SUPERUSER_PASSWORD'])

    # Coach
    try:
        Coach.objects.get(email='coach@conners.com')
    except ObjectDoesNotExist:
        Coach.objects.create_superuser(
            first_name='Coach', last_name='Conners', password=environ['DJANGO_SUPERUSER_PASSWORD'], email='coach@conners.com', is_admin=False)
