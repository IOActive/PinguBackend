# Pingu Backend

The project offers the following features:

* Pingu API that allows to perform various backend fuzzing related tasks such as storing crashes information, fuzzer targets etc.
* Pingu Backend uses Mongo database to stores all the data related to the project.
* A Celery worker that runs asynchronous tasks in the background, which helps improve the performance of the application by allowing multiple tasks to be executed simultaneously.
* A RabbitMQ queue that stores the tasks to be executed by the Celery worker and the bot instaces, ensuring that the tasks are executed in order and ensuring the smooth functioning of the application.
* Additionally, the Minio Bucket Service  provides an on-demand storage solution for the application, allowing to temporal store and retrieve data quickly and easily.

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

### Python dependencies

```bash
pip install -r requeriments 
```

### Secondary services

The easyest way to run all the secundary services is by using docker containers. The docker-compose files include a production and testing configuration for you to deploy the MongoDb, RabbitMq and the Minio Buckets

# Run server

```
python manage.py makemigrations --settings=PinguBackend.settings.development
python manage.py migrate --settings=PinguBackend.settings.development
python manage.py runserver 0.0.0.0:8080 --settings=PinguBackend.settings.development

python manage.py createsuperuser

```

## API Documentation

By default the Swagger UI is enable in the backend for testing propueses, there you can find all the API documentation and interacte live this all the requests. Additionally, the API is also documented [here](docs/api.md "docs/api.md")

## MongoDB schema

## Misc

Export MongoDb schema

```bash
mongo-schema-export.py --uri mongodb://127.0.0.1:27017/ --database 

pingu_dbmongo-schema-import.py --uri mongodb://127.0.0.1:27017/ --databases pingu_db --verbose --delete-col
```
