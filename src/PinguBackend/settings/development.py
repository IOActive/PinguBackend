# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PinguBackend.settings.base import *
from decouple import config
from django.utils import timezone

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "auth_db",
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    },
    "primary": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "primary_db",
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    },
    "bigquery": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": "bigquery_db",
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    },
}

ALLOWED_HOSTS = ['*']

QUEUE_HOST = config("QUEUE_HOST")

CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_TIMEZONE = timezone.get_current_timezone()

CORS_ORIGIN_ALLOW_ALL = True
#CORS_ORIGIN_WHITELIST = (f"http://{config("BACKEND_HOST")}:{config("BACKEND_PORT")}",)

# Storage settings
## Bucktes Minio variables
MINIO_HOST = f"{config("MINIO_HOST")}:{config("MINIO_API_PORT")}"
MINIO_ACCESS_KEY = config("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = config("MINIO_SECRET_KEY")

## Local Storage variables
LOCAL_STORAGE_PATH = config("LOCAL_STORAGE_PATH")

# Sever Settings
SERVER_HOST = config("BACKEND_HOST")
SERVER_PORT = config("BACKEND_PORT")


# Override default port for `runserver` command
from django.core.management.commands.runserver import Command as runserver

runserver.default_port = SERVER_PORT
runserver.default_addr = SERVER_HOST

