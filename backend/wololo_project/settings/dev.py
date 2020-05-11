from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

ASGI_APPLICATION = 'wololo_project.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wololodjango',
        'USER': 'postgres',
        'PASSWORD': '5428',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
