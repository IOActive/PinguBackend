from PinguBackend.settings.base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DEBUG = True

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

#Bucktes Minio variables
MINIO_HOST = '127.0.0.1:9000'
ACCESS_KEY = 'mK6kUOlDZ834q0wL'
SECRET_KEY = 'Hq1cuslNaaAFcLXU6q45fqhrFGFG3UCO'