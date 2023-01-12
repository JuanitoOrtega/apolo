from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        # 'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = [
    'config/static/',
]

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = 'media/'