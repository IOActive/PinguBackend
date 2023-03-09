from PinguBackend.settings.development import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'pingu_db',
        'HOST': 'database',
        'PORT': 27017,
    }
}

QUEUE_HOST = 'queue'
CELERY_BROKER_URL = 'amqp://queue'
