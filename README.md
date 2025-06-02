# Pingu Backend

The project offers the following features:

* Pingu API that allows to perform various backend fuzzing related tasks such as storing crashes information, fuzzer targets etc.
* Pingu Backend uses Postgres database to store all the data related to the project.
* A Celery worker that runs asynchronous tasks in the background, which helps improve the performance of the application by allowing multiple tasks to be executed simultaneously.
* A RabbitMQ queue that stores the tasks to be executed by the Celery worker and the bot instances, ensuring that the tasks are executed in order and ensuring the smooth functioning of the application.
* Bucket storage provides an on-demand storage solution for the application, allowing temporal storage and retrieval of data quickly and easily.

---

## Documentation Index

| Document                | Description                                      |
|-------------------------|--------------------------------------------------|
| [Setup](docs/setup.md)  | Instructions for setting up the backend locally and with Docker. |
| [Database](docs/database.md) | Details on database setup, configuration, and usage. |
| [Bucket Storage](docs/bucket_storage.md) | Configuration and usage of Minio and File System storage providers. |
| [Async Tasks](docs/async_tasks.md) | Setup and management of asynchronous tasks using Celery. |
| [API Reference](docs/api.md) | Detailed API documentation for all endpoints. |