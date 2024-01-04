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
ACCESS_KEY = config('ACCESS_KEY')
SECRET_KEY = config('SECRET_KEY')