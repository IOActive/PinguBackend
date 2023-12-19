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

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8081',
)

#Bucktes Minio variables
MINIO_HOST = '127.0.0.1:9000'
ACCESS_KEY = 'xS4vswhnoH8FYgIU'
SECRET_KEY = 'kWvETRF3CN8MTU89BDIE3uIrgzVMh0OR'