from PinguBackend.settings.base import *
from decouple import config

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

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8081',
)

#Bucktes Minio variables
MINIO_HOST = config('MINIO_HOST')
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY')
