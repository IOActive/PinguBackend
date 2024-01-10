from PinguBackend.settings.base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DEBUG = True

DATABASES = {
    'default': {
      'ENGINE': 'djongo',
      'NAME': 'pingu_db',
      'CLIENT': {
          'host': config('MONGO_HOST'),
      }
  }
}

QUEUE_HOST = config('QUEUE_HOST')
CELERY_BROKER_URL = config('CELERY_BROKER_URL')

#Bucktes Minio variables
MINIO_HOST = config('MINIO_HOST')
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY')