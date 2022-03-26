"""
Django settings for production.

Created to run on "sel2-5.ugent.be" domain.
"""
from .common import *  # noqa
import os
# Import development environment

# General
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['sel2-5.ugent.be']

CSRF_TRUSTED_ORIGINS = ['https://sel2-5.ugent.be']

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