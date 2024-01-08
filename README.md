# Basic configuration

You will need to create a .env to store your secrets. Eg,:

* Docker dev example
```Python
SECRET_KEY="XXXXXX"
MINIO_HOST = '127.0.0.1:9000'
ACCESS_KEY = 'mK6kUOlDZ834q0wL'
SECRET_KEY = 'Hq1cuslNaaAFcLXU6q45fqhrFGFG3UCO'
QUEUE_HOST = 'queue'
CELERY_BROKER_URL = 'amqp://queue'
MONGO_HOST = 'mongodb://localhost:27017/'
MONGO_DB_PATH = '/home/xxxx/mounting_point/src/database'
MINIO_ROOT_USER = 'minioadmin'
MINIO_ROOT_PASSWORD = 'minioadmin'
MINIO_STORAGE_PATH = '/home/xxxx/mounting_point/src/minio'
```

# Install requeriments

# Run server
```
python manage.py makemigrations --settings=PinguBackend.settings.development
python manage.py migrate --settings=PinguBackend.settings.development
python manage.py runserver 0.0.0.0:8080 --settings=PinguBackend.settings.development

python manage.py createsuperuser

```
