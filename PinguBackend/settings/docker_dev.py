from PinguBackend.settings.base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
      'ENGINE': 'djongo',
      'NAME': 'pingu_db',
      'CLIENT': {
          'host': 'mongodb://database:27017',
      }
  }
}

QUEUE_HOST = 'queue'
CELERY_BROKER_URL = 'amqp://queue'
