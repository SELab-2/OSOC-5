"""
Django settings for development.
"""
from os import getenv
from .common import *  # noqa

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)glohf%v3h(8%5&zqfc)k*69&nz1!4bn#1g1s3_ndvf$zt37&4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'localhost:8000',
                 '0.0.0.0', '127.0.0.1', 'sel2-5.ugent.be']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', 'https://sel2-5.ugent.be',
]
CORS_ALLOW_CREDENTIALS = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'dev',
        'HOST': getenv('POSTGRES_HOST', 'db'),
        'PORT': 5432,
    }
}
