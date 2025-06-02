# Database Setup and Configuration

This document provides details on the database setup, configuration, and usage in the PinguCrew backend.

---

## Supported Databases

The system supports the following databases:
1. **PostgreSQL**: Used for primary and authentication data.
2. **TimescaleDB**: Used for time-series data and analytics.

---

## Configuration

The database configuration is located in `config/database/config.yaml`. Update the following fields as needed:

```yaml
env:
  POSTGRES_USER: postgres # CHANGE IT !!!
  POSTGRES_PASSWORD: postgres # CHANGE IT !!!
  POSTGRES_HOST: localhost
  POSTGRES_PORT: 5432
```

---

## Database Router

The system uses a custom database router (`db_router.py`) to route queries to the appropriate database. The routing logic is as follows:

- **Primary Database**: Handles most of the application data.
- **BigQuery Database**: Handles time-series data for analytics.
- **Default Database**: Used for other operations such a user managment.

### Router Logic

- **Read Operations**: Queries are routed based on the model's app label and name.
- **Write Operations**: Writes are routed similarly to reads.
- **Migrations**: Models are migrated to their respective databases.

---

## Local Development Setup

1. **Start the Database**

   Use the provided `docker-compose.yml` file to start the database services:

   ```bash
   docker-compose up database
   ```
---

## TimescaleDB

TimescaleDB is used for handling time-series data. It is built on top of PostgreSQL and provides additional features for analytics.

### Configuration

TimescaleDB is configured as a separate database (`bigquery`) in the system. Ensure the following settings are correct in `development.py`:

```python
DATABASES = {
    "bigquery": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": "bigquery_db",
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),minio_access_token
    },
}
```

---

## Notes

- Use secure credentials for production environments.
- Ensure the database services are running before starting the backend.