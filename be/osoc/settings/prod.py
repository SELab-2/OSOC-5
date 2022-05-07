"""
Django settings for production.

Created to run on "sel2-5.ugent.be" domain.
"""
# pylint: disable=wildcard-import,unused-wildcard-import
import os
from .common import *  # noqa
# Import development environment

# General
DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['sel2-5.ugent.be']

SESSION_COOKIE_DOMAIN = 'sel2-5.ugent.be/api'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': 5432,
    }
}
