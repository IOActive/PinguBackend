from PinguBackend.settings.base import *

DATABASES = {
    'default': {
      'ENGINE': 'djongo',
      'NAME': 'pingu_db',
      'CLIENT': {
          'host': 'mongodb://localhost:27017/',
      }
  }
}

QUEUE_HOST = 'localhost'
CELERY_BROKER_URL = 'amqp://localhost'
    