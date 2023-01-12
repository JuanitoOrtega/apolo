from .base import *

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['5.78.43.135', 'pos.juanitodev.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}