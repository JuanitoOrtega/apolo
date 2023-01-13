from .settings import *

<<<<<<< HEAD:config/production.py
DEBUG = True

ALLOWED_HOSTS = ['pos.juanitodev.com']
=======
ALLOWED_HOSTS = ['5.78.43.135', 'pos.juanitodev.com']
>>>>>>> deployment:config/settings/production.py

DEBUG = False

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
